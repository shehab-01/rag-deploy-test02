from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np


def get_embedding_function(language):
    if language == "ko":
        return get_korean_embedding_function()
    else:
        return get_english_embedding_function()


def get_korean_embedding_function():
    embeddings = HuggingFaceEmbeddings(
        model_name="jhgan/ko-sroberta-nli", model_kwargs={"device": "cuda"}, encode_kwargs={"normalize_embeddings": True}
    )
    return lambda text: np.array(embeddings.embed_query(text))


def get_english_embedding_function():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": "cuda"}, encode_kwargs={"normalize_embeddings": True}
    )
    return lambda text: np.array(embeddings.embed_query(text))
