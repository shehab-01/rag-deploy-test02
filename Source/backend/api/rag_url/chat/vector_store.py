# good

from pymilvus import connections, Collection, DataType, FieldSchema, CollectionSchema, utility
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
from tqdm import tqdm

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Initialize the Korean SRoBERTa model
model = SentenceTransformer("jhgan/ko-sroberta-nli")
model = model.to(device)

# Milvus connection parameters
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
COLLECTION_NAME = "memebox_20141018"


def create_embeddings(texts):
    """
    Create embeddings for the given texts using the Korean SRoBERTa model.
    """
    with torch.no_grad():
        embeddings = model.encode(texts, convert_to_tensor=True, device=device, show_progress_bar=False)
    return embeddings.cpu().numpy()


def add_to_milvus(vectors, texts):
    """
    Add the given rows to the Milvus collection.
    """
    # Connect to Milvus
    connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

    # Check if collection exists, if not, create it
    if not utility.has_collection(COLLECTION_NAME):
        create_milvus_collection()

    # Get the collection
    collection = Collection(COLLECTION_NAME)

    # Insert the data
    collection.insert([vectors, texts])

    # Flush the collection to ensure data is visible for search
    collection.flush()


def create_milvus_collection():
    """
    Create the Milvus collection if it doesn't exist.
    """
    # Get the dimension of the embedding
    sample_embedding = create_embeddings(["샘플 텍스트"])[0]
    dim = len(sample_embedding)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
    ]

    schema = CollectionSchema(fields, "Document chunks collection")
    collection = Collection(COLLECTION_NAME, schema)

    # Create an IVF_FLAT index for the vector field
    index_params = {"metric_type": "L2", "index_type": "IVF_FLAT", "params": {"nlist": 1024}}
    collection.create_index("vector", index_params)

    print(f"Created Milvus collection: {COLLECTION_NAME}")


def search_milvus(query_text, top_k=5):
    """
    Search the Milvus collection for the most similar vectors.
    """
    connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
    collection = Collection(COLLECTION_NAME)
    collection.load()

    # Create embedding for the query text
    query_vector = create_embeddings([query_text])[0]

    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search(data=[query_vector], anns_field="vector", param=search_params, limit=top_k, output_fields=["text"])

    return results
