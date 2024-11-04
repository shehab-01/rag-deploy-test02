import torch
from sentence_transformers import SentenceTransformer, util
from pymilvus import connections, Collection
import pandas as pd
from fuzzywuzzy import fuzz

# from q_extension import expand_query
# from prompts_collection import get_system_instruction, get_user_prompt_template
# from api_helper import send_open_api, send_open_api_stream, send_request
from langchain.prompts import ChatPromptTemplate

from api.rag_url.chat.q_extension import expand_query
from api.rag_url.chat.prompts_collection import get_system_instruction, get_user_prompt_template
from api.rag_url.chat.api_helper import send_open_api, send_open_api_stream, send_request

# Milvus connection parameters
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
# COLLECTION_NAME = 'amoremall_vectordb_20141016'
# COLLECTION_NAME = "memebox_20141018"
COLLECTION_NAME = "amore_new"


class EmbeddingModel:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None

    def load_model(self):
        if self.model is None:
            self.model = SentenceTransformer("jhgan/ko-sroberta-nli")
            self.model = self.model.to(self.device)

    def create_embeddings(self, texts):
        self.load_model()
        with torch.no_grad():
            embeddings = self.model.encode(texts, convert_to_tensor=True, device=self.device, show_progress_bar=True)
        return embeddings.cpu().numpy()


embedding_model = EmbeddingModel()


qa_df = pd.read_excel("C:\\python\\nuxt-fastapi_\\\Source\\backend\\api\\rag_url\\chat\\basic_qa.xlsx")


def search_milvus(query_text, top_k=20):
    connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
    collection = Collection(COLLECTION_NAME)
    collection.load()

    query_vector = embedding_model.create_embeddings([query_text])[0]

    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search(data=[query_vector], anns_field="embedding", param=search_params, limit=top_k, output_fields=["text"])

    return results


def rerank_results(query, results, top_k):
    query_embedding = embedding_model.model.encode(query, convert_to_tensor=True, device=embedding_model.device)  # change to vector for memebox

    reranked_results = []
    seen_texts = set()

    for hit in results[0]:
        text = hit.entity.get("text")
        if text in seen_texts:
            continue

        text_embedding = embedding_model.model.encode(text, convert_to_tensor=True, device=embedding_model.device)
        similarity = util.pytorch_cos_sim(query_embedding, text_embedding).item()

        reranked_results.append((text, similarity))
        seen_texts.add(text)

    reranked_results.sort(key=lambda x: x[1], reverse=True)
    return reranked_results[:top_k]


def check_basic_qa(question):
    for _, row in qa_df.iterrows():
        if fuzz.ratio(question.lower(), row["Question"].lower()) > 85:
            return row["Answer"]
    return None


def answer_question(question, top_k=5):
    basic_answer = check_basic_qa(question)
    if basic_answer:
        print("Excel 피일에서 답 가져옵니다.")
        return basic_answer

    print("Excel 피일에서 답 찾을 수 없읍니다.")
    expand_querys = expand_query(question)
    final_query = question + expand_querys
    # print(final_query)

    initial_results = search_milvus(final_query, top_k * 3)
    # print("Initial: ",initial_results)
    print("Reranking results...")
    reranked_results_ = rerank_results(final_query, initial_results, top_k)
    # print(reranked_results_)

    # new
    PROMPT_TEMPLATE = get_user_prompt_template()
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(question=final_query, context=reranked_results_)
    system_instruction = get_system_instruction()

    # OpenApi
    stream = send_open_api_stream(system_instruction, prompt)
    return stream

    # LLAMA local
    # result = send_request(system_instruction, prompt)
    # return result


def ask_ai(final_query, reranked_results_):
    PROMPT_TEMPLATE = get_user_prompt_template()
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(question=final_query, context=reranked_results_)
    system_instruction = get_system_instruction()
    response = send_open_api(system_instruction, prompt)
    return response


# async def search_query_ai():
#     question = "아이 섀도 모가 좋아?"
#     print(f"Question: {question}")

#     answer = answer_question(question)
#     # print("Answer:")
#     # # print(answer)
#     # for chunk in answer:
#     #     if chunk.choices[0].delta.content is not None:
#     #         print(chunk.choices[0].delta.content, end="", flush=True)
#     # print()

#     return answer


async def search_query_ai(question: str):
    print(f"Question: {question}")
    answer = answer_question(question)
    return answer
