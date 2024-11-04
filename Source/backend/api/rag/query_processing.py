import logging
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from sentence_transformers import CrossEncoder
from rank_bm25 import BM25Okapi
from typing import List
import numpy as np
from langchain.schema import Document
from deep_translator import GoogleTranslator
import json
from api.database.db_helper import db_helper
from api.rag.nlu import process_query_nlu
from api.rag.utils import get_safe_path, convert_to_json_serializable
from api.rag.embedding import get_embedding_function
import io
import faiss
import pickle
import os
import tempfile


def deserialize_faiss_index(index_bytes):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(index_bytes)
        temp_file_path = temp_file.name

    try:
        index = faiss.read_index(temp_file_path)
    finally:
        os.unlink(temp_file_path)

    return index


def reciprocal_rank_fusion(results_list: List[List[Document]], k=60):
    fused_scores = {}
    for results in results_list:
        for rank, doc in enumerate(results):
            doc_id = doc.metadata.get("id")
            if doc_id not in fused_scores:
                fused_scores[doc_id] = 0
            fused_scores[doc_id] += 1 / (rank + k)

    sorted_docs = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    return [doc_id for doc_id, score in sorted_docs]


def bm25_search(query: str, documents: List[Document], top_k=10):
    logging.info(f"BM25 search called with query: '{query}' and {len(documents)} documents")

    corpus = []
    for i, doc in enumerate(documents):
        if not isinstance(doc, Document):
            logging.warning(f"Item {i} is not a Document object. Type: {type(doc)}")
            continue

        if not hasattr(doc, "page_content") or not isinstance(doc.page_content, str):
            logging.warning(f"Document {i} has invalid page_content. Type: {type(getattr(doc, 'page_content', None))}")
            continue

        content = doc.page_content.strip()
        logging.info(f"Document {i} content (first 100 chars): {repr(content[:100])}")

        if content:
            corpus.append(content.split())
            logging.info(f"Document {i} added to corpus. Word count: {len(corpus[-1])}")
        else:
            logging.warning(f"Document {i} has empty content after stripping")
            corpus.append(["EMPTY_DOCUMENT"])  # Add a placeholder for empty documents

    logging.info(f"Corpus created with {len(corpus)} documents")

    if not corpus:
        logging.warning("BM25 search received an empty corpus. Returning an empty list.")
        return []

    try:
        bm25 = BM25Okapi(corpus)
        tokenized_query = query.split()
        doc_scores = bm25.get_scores(tokenized_query)

        logging.info(f"BM25 scores calculated. Min score: {min(doc_scores)}, Max score: {max(doc_scores)}")

        top_n = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_k]
        results = [documents[i] for i in top_n]

        logging.info(f"BM25 search completed. Returning {len(results)} results.")
        for i, doc in enumerate(results[:3]):  # Log details of top 3 results
            logging.info(f"Top result {i+1}: Score: {doc_scores[top_n[i]]}, First 50 chars: {repr(doc.page_content[:50])}")

        return results
    except Exception as e:
        logging.error(f"Error in BM25 search: {str(e)}", exc_info=True)
        return []


def get_prompt_template(language):
    if language == "ko":
        return """
        주어진 컨텍스트만을 사용하여 질문에 답변하세요. 컨텍스트에 없는 정보로 절대 답변하지 마세요.

        컨텍스트:
        {context}

        질문: {question}
        의도: {intent}
        주요 개체: {entities}

        지시사항:
        1. 먼저, 질문에 대한 답변이 컨텍스트에 있는지 확인하세요.
        2. 컨텍스트에 "Table Summaries:" 섹션이 있다면, 이 정보를 우선적으로 고려하세요. 사용자가 명시적으로 표에 대해 묻지 않더라도 이 정보가 관련이 있다면 반드시 포함시키세요.
        3. 답변이 컨텍스트에 있다면, 관련 정보를 찾아 명확하고 간결하게 답변하세요.
        4. 질문의 의도와 주요 개체를 고려하여 답변을 구성하세요.
        5. 답변이 컨텍스트에 없다면, 반드시 다음과 같이 답하세요: "죄송합니다. 주어진 컨텍스트에서 이 질문에 대한 답변을 찾을 수 없습니다."
        6. 부분적인 정보만 있다면 추측하지 말고 그 정보만 사용하세요.

        제약사항:
        - 컨텍스트에 없는 정보로 절대 답변하지 마세요.
        - "컨텍스트에 따르면" 등의 문구를 사용하지 마세요.
        - 질문과 무관한 정보는 포함하지 마세요.

        답변:
        """
    else:
        return """
        Answer the question using only the given context. Do not use information from outside the context.

        Context:
        {context}

        Question: {question}
        Intent: {intent}
        Key Entities: {entities}

        Instructions:
        1. First, check if the answer to the question is in the context.
        2. If there's a "Table Summaries:" section in the context, prioritize this information. Include it in your answer if relevant, even if the user didn't explicitly ask about table information.
        3. If the answer is in the context, find the relevant information and answer clearly and concisely.
        4. Consider the question's intent and key entities when formulating your answer.
        5. If the answer is not in the context, respond with: "I'm sorry, but I couldn't find an answer to that question in the provided context."
        6. If only partial information is available, use only that information without making assumptions.

        Constraints:
        - Do not use any information that is not in the context.
        - Do not use phrases like "According to the context" or similar.
        - Do not include information unrelated to the question.

        Answer:
        """


def get_cross_encoder(language):
    if language == "ko":
        return CrossEncoder("bongsoo/klue-cross-encoder-v1")
    else:
        return CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


async def process_query(query_text: str, directory_name: str, question_language: str):
    try:
        logging.info(f"Processing query: '{query_text}' for directory: {directory_name}")
        nlu_result = process_query_nlu(query_text, question_language)
        query_language = nlu_result["language"]

        logging.info(f"NLU Result: {nlu_result}")

        # Load child index
        child_faiss_bytes, child_pkl_bytes = db_helper.load_faiss_from_postgres(f"{directory_name}_child")
        logging.info(f"Child FAISS bytes loaded. Length: {len(child_faiss_bytes)}")
        logging.info(f"Child PKL bytes loaded. Length: {len(child_pkl_bytes)}")

        try:
            child_index = deserialize_faiss_index(child_faiss_bytes)
            logging.info("Child FAISS index deserialized successfully")
        except Exception as e:
            logging.error(f"Error deserializing child index: {str(e)}")
            raise

        child_metadata = pickle.loads(child_pkl_bytes)
        logging.info(f"Child metadata loaded. Number of items: {len(child_metadata)}")

        if child_metadata:
            logging.info(f"Sample child metadata keys: {list(child_metadata[0].keys())}")
            logging.info(f"Sample child metadata values: {child_metadata[0]}")
            document_language = child_metadata[0].get("language", "unknown")
            logging.info(f"Document language: {document_language}")
        else:
            logging.warning("Child metadata is empty")
            document_language = "unknown"

        embedding_function = get_embedding_function(document_language)

        if query_language != document_language:
            translator = GoogleTranslator(source=query_language, target=document_language)
            translated_query = translator.translate(query_text)
            expanded_query = process_query_nlu(translated_query, query_language)["expanded_query"]
            logging.info(f"Translated query from {query_language} to {document_language}: {translated_query}")
        else:
            expanded_query = nlu_result["expanded_query"]

        logging.info(f"Expanded query: {expanded_query}")

        # Perform similarity search on child index
        query_vector = embedding_function(expanded_query)
        logging.info(f"Query vector type: {type(query_vector)}")
        logging.info(f"Query vector shape: {query_vector.shape}")

        D, I = child_index.search(query_vector.reshape(1, -1), k=20)
        logging.info(f"FAISS search results - Distances: {D}")
        logging.info(f"FAISS search results - Indices: {I}")

        semantic_results = []
        for i, idx in enumerate(I[0]):
            if idx < len(child_metadata):
                metadata = child_metadata[idx]
                page_content = metadata.get("page_content", "")
                logging.info(f"Document {i} (index {idx}) raw content: {repr(page_content)}")
                logging.info(f"Document {i} (index {idx}) content length: {len(page_content)}")
                logging.info(f"Document {i} (index {idx}) metadata keys: {metadata.keys()}")

                for key, value in metadata.items():
                    logging.info(f"Document {i} (index {idx}) metadata['{key}']: {repr(value)}")

                doc = Document(page_content=page_content, metadata=metadata)
                semantic_results.append(doc)
            else:
                logging.warning(f"Index {idx} is out of range for child_metadata (length: {len(child_metadata)})")

        logging.info(f"Number of semantic results: {len(semantic_results)}")
        if semantic_results:
            logging.info(f"Sample semantic result metadata: {semantic_results[0].metadata}")
            logging.info(f"Sample semantic result page content (first 100 chars): {semantic_results[0].page_content[:100]}")
        else:
            logging.warning("No semantic results found")

        # Perform MMR search (placeholder)
        mmr_results = semantic_results
        logging.info(f"Number of MMR results: {len(mmr_results)}")

        # Prepare documents for BM25 search
        bm25_docs = semantic_results + mmr_results
        logging.info(f"Number of documents for BM25 search: {len(bm25_docs)}")

        if bm25_docs:
            for i, doc in enumerate(bm25_docs[:5]):  # Log details of first 5 documents
                logging.info(f"BM25 document {i} metadata: {doc.metadata}")
                logging.info(f"BM25 document {i} content (first 100 chars): {doc.page_content[:100]}")
        else:
            logging.warning("No documents available for BM25 search")

        # Perform BM25 search
        logging.info(f"Calling BM25 search with query: '{expanded_query}' and {len(bm25_docs)} documents")
        keyword_results = bm25_search(expanded_query, bm25_docs, top_k=20)
        logging.info(f"Number of keyword results from BM25 search: {len(keyword_results)}")

        fused_ids = reciprocal_rank_fusion([semantic_results, mmr_results, keyword_results])
        fused_results = [doc for doc in semantic_results + mmr_results + keyword_results if doc.metadata.get("id") in fused_ids]
        logging.info(f"Number of fused results: {len(fused_results)}")

        reranker = get_cross_encoder(document_language)
        child_scores = reranker.predict([(expanded_query, doc.page_content) for doc in fused_results])
        reranked_children = [doc for _, doc in sorted(zip(child_scores, fused_results), key=lambda x: x[0], reverse=True)][:10]
        logging.info(f"Number of reranked children: {len(reranked_children)}")

        parent_ids = list(set([child.metadata["parent_id"] for child in reranked_children]))
        logging.info(f"Number of unique parent IDs: {len(parent_ids)}")

        # Load parent index
        parent_faiss_bytes, parent_pkl_bytes = db_helper.load_faiss_from_postgres(f"{directory_name}_parent")
        logging.info(f"Parent FAISS bytes loaded. Length: {len(parent_faiss_bytes)}")
        logging.info(f"Parent PKL bytes loaded. Length: {len(parent_pkl_bytes)}")

        try:
            parent_index = deserialize_faiss_index(parent_faiss_bytes)
            logging.info("Parent FAISS index deserialized successfully")
        except Exception as e:
            logging.error(f"Error deserializing parent index: {str(e)}")
            raise

        parent_metadata = pickle.loads(parent_pkl_bytes)
        logging.info(f"Parent metadata loaded. Number of items: {len(parent_metadata)}")

        parent_results = [
            Document(page_content=meta.get("page_content", ""), metadata=meta) for meta in parent_metadata if meta.get("id") in parent_ids
        ]
        logging.info(f"Number of parent results: {len(parent_results)}")

        if parent_results:
            logging.info(f"Sample parent result metadata: {parent_results[0].metadata}")
            logging.info(f"Sample parent result page content (first 100 chars): {parent_results[0].page_content[:100]}")
        else:
            logging.warning("No parent results found")

        parent_scores = reranker.predict([(expanded_query, doc.page_content) for doc in parent_results])
        reranked_parents = [doc for _, doc in sorted(zip(parent_scores, parent_results), key=lambda x: x[0], reverse=True)]
        logging.info(f"Number of reranked parents: {len(reranked_parents)}")

        context_docs = reranked_parents[:5]
        context_text = "\n\n---\n\n".join([doc.page_content for doc in context_docs])
        logging.info(f"Context text length: {len(context_text)}")
        logging.debug(f"Context text (first 500 chars): {context_text[:500]}...")

        PROMPT_TEMPLATE = get_prompt_template(document_language)
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(
            context=context_text,
            question=expanded_query,
            intent=nlu_result["intent"] if nlu_result["intent"] != "NEGATIVE" else "General Query",
            entities=", ".join([e["word"] for e in nlu_result["entities"]]) if nlu_result["entities"] else "No specific entities detected",
        )

        model = Ollama(model="llama3.1:8b", temperature=0.25)
        initial_response = model.invoke(prompt)

        logging.info("Initial response generated")

        if query_language != document_language:
            translator = GoogleTranslator(source=document_language, target=query_language)
            initial_response = translator.translate(initial_response)
            logging.info(f"Translated response from {document_language} to {query_language}")

        sources = []
        seen_ids = set()

        for doc in context_docs + reranked_children:
            doc_id = doc.metadata.get("id")
            if doc_id not in seen_ids:
                seen_ids.add(doc_id)
                sources.append(
                    {
                        "id": doc_id,
                        "page": doc.metadata.get("page"),
                        "chunk_type": doc.metadata.get("chunk_type"),
                        "parent_id": doc.metadata.get("parent_id") if doc.metadata.get("chunk_type") == "child" else doc_id,
                    }
                )

        result_dict = {
            "initial_response": initial_response,
            "sources": sources,
            "nlu_info": {
                "intent": nlu_result["intent"],
                "entities": nlu_result["entities"],
                "original_language": query_language,
                "document_language": document_language,
                "translation_applied": query_language != document_language,
            },
        }

        logging.info("Query processing completed successfully")
        return convert_to_json_serializable(result_dict)

    except Exception as e:
        logging.error(f"Error in process_query: {str(e)}", exc_info=True)
        raise
