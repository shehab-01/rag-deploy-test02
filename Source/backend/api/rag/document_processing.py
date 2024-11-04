import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
import tabula
from langchain_community.llms.ollama import Ollama
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
from langdetect import detect
from api.rag.vector_store import add_to_faiss
from api.rag.utils import get_safe_path
from api.database.db_helper import db_helper


def load_documents(data_path):
    document_loader = PyPDFDirectoryLoader(data_path)
    return document_loader.load()


def split_documents(documents: list[Document]):
    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200, chunk_overlap=100, separators=["\n\n", "\n", "(?<=\. )", " ", ""], length_function=len
    )
    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512, chunk_overlap=50, separators=["\n\n", "\n", "(?<=\. )", " ", ""], length_function=len
    )

    parent_chunks = parent_splitter.split_documents(documents)

    all_chunks = []
    for i, parent in enumerate(parent_chunks):
        parent.metadata["chunk_type"] = "parent"
        parent.metadata["parent_id"] = f"p{i}"
        all_chunks.append(parent)

        children = child_splitter.split_text(parent.page_content)
        for j, child_text in enumerate(children):
            child = Document(page_content=child_text, metadata={**parent.metadata})
            child.metadata["chunk_type"] = "child"
            child.metadata["child_id"] = f"p{i}_c{j}"
            all_chunks.append(child)

    return all_chunks


def detect_language(text):
    try:
        return detect(text)
    except:
        return "ko"


def calculate_chunk_ids(chunks):
    for chunk in chunks:
        if chunk.metadata["chunk_type"] == "parent":
            chunk.metadata["id"] = chunk.metadata["parent_id"]
        else:
            chunk.metadata["id"] = chunk.metadata["child_id"]
    return chunks


def extract_and_summarize_tables(pdf_path, page_number, language):
    tables = tabula.read_pdf(pdf_path, pages=page_number, multiple_tables=True)
    summaries = []
    for table in tables:
        # print("table:", table)
        # enriched_table = enrich_table(table)
        summary = summarize_table(table, Ollama(model="llama3.1:8b", temperature=0), language)
        summaries.append(summary)
    # print("Summary: ",summaries)
    return "\n\n".join(summaries)


def enrich_table(table):
    headers = table.columns.tolist()
    enriched_data = []
    for _, row in table.iterrows():
        enriched_row = [f"{header}: {value}" for header, value in zip(headers, row)]
        enriched_data.append(" | ".join(enriched_row))
    return "\n".join(enriched_data)


def summarize_table(enriched_table, model, language):
    if language == "en":
        prompt = f"""
            You are tasked with summarizing the following table data. This data is from a structured table, where each line represents a row. The format is 'Column Name: Value'.

            Table Data:
            {enriched_table}

            Instructions:
            1. Treat this as tabular data, not free-form text.
            2. Do not skip or omit any information from the table.
            3. Provide a comprehensive summary that includes all columns and their values.
            4. If there are multiple rows, describe patterns or trends you observe.
            5. Use precise language and maintain the original terminology used in the table.
            6. If numerical data is present, include key statistics (e.g., highest, lowest, average values) if applicable.
            7. Your summary should be structured and easy to read, but also complete.

            Summarize the table data following these instructions:
        """
    else:
        prompt = f"""
            다음의 표 데이터를 요약하는 작업을 수행하십시오. 이 데이터는 구조화된 표에서 가져온 데이터입니다. 형식은 '열 이름: 값'입니다.

            표 데이터:
            {enriched_table}

            지시사항:
            1. 이것을 자유 형식의 텍스트가 아닌 표 형식의 데이터로 취급하십시오.
            2. 표의 어떤 정보도 생략하거나 누락하지 마십시오.
            3. 모든 열과 그 값을 포함하는 포괄적인 요약을 제공하십시오.
            4. 여러 행이 있는 경우, 관찰되는 패턴이나 경향을 설명하십시오.
            5. 정확한 언어를 사용하고 표에서 사용된 원래의 용어를 유지하십시오.
            6. 수치 데이터가 있는 경우, 해당되는 경우 주요 통계(예: 최고값, 최저값, 평균값)를 포함하십시오.
            7. 요약은 구조화되고 읽기 쉬워야 하지만 동시에 완전해야 합니다.

            이러한 지시사항을 따라 표 데이터를 요약하십시오:
        """

    summary = model.invoke(prompt)
    return summary


async def process_documents(directory, docLanguage):
    print("before creating table")
    # db_helper.create_rag_vectors_table()
    DATA_PATH = f"data/{directory}"

    print(f"Data Path: {DATA_PATH}")

    documents = load_documents(DATA_PATH)
    sample_text = documents[0].page_content[:1000]

    language = docLanguage

    chunks = split_documents(documents)
    chunks_with_ids = calculate_chunk_ids(chunks)

    for chunk in chunks_with_ids:
        chunk.metadata["language"] = language

    try:
        result = add_to_faiss(chunks_with_ids, directory, language)
        return "Embedding complete"
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return f"Error: {str(e)}"


async def process_documents01(directory, docLanguage):
    FAISS_PATH = get_safe_path(directory)
    DATA_PATH = f"data/{directory}"

    print(f"FAISS Path: {FAISS_PATH}, Data Path: {DATA_PATH}")

    documents = load_documents(DATA_PATH)
    sample_text = documents[0].page_content[:1000]

    # sample_text = ""
    # for index in range(5):
    #     sample_text + str(documents[index].page_content[:1000])

    language = docLanguage

    # processed_documents = []
    # for doc in documents:

    #     table_summaries = extract_and_summarize_tables(doc.metadata['source'], doc.metadata['page'], language)

    #     combined_content = f"{doc.page_content}\n\nTable Summaries:\n{table_summaries}"

    #     processed_doc = Document(
    #         page_content=combined_content,
    #         metadata=doc.metadata
    #     )
    #     processed_documents.append(processed_doc)
    #     print("Processed Document:")
    #     print(f"Source: {processed_doc.metadata['source']}")
    #     print(f"Page: {processed_doc.metadata['page']}")
    #     print(f"Content preview: {processed_doc.page_content}...")  # Print first 200 characters
    #     print("-------------------")

    # print(f"Detected language: {language}")
    # print(f"Total processed documents: {len(processed_documents)}")
    # chunks = split_documents(documents)
    # chunks = split_documents(processed_documents)
    chunks = split_documents(documents)
    chunks_with_ids = calculate_chunk_ids(chunks)

    for chunk in chunks_with_ids:
        chunk.metadata["language"] = language

    try:
        add_to_faiss(chunks_with_ids, FAISS_PATH, language)
        return "Embedding complete"
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return f"Error: {str(e)}"
