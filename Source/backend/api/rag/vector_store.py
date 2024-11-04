import numpy as np
from api.rag.embedding import get_embedding_function
from api.database.db_helper import db_helper
from api.rag.utils import convert_to_json_serializable
import faiss
import tempfile
import os
import pickle
import logging
from api.common import exceptions as ex


def add_to_faiss(chunks, directory_name, language):
    logging.info(f"Adding chunks to FAISS for directory: {directory_name}, language: {language}")
    embedding_function = get_embedding_function(language)

    parent_chunks = [chunk for chunk in chunks if chunk.metadata["chunk_type"] == "parent"]
    child_chunks = [chunk for chunk in chunks if chunk.metadata["chunk_type"] == "child"]

    logging.info(f"Number of parent chunks: {len(parent_chunks)}")
    logging.info(f"Number of child chunks: {len(child_chunks)}")

    try:
        # Create and store parent index
        parent_vectors = np.array(embedding_function.embed_documents([chunk.page_content for chunk in parent_chunks]), dtype=np.float32)
        parent_index = faiss.IndexFlatL2(parent_vectors.shape[1])
        parent_index.add(parent_vectors)

        # Serialize parent index
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            faiss.write_index(parent_index, temp_file.name)
            temp_file.seek(0)
            parent_faiss_bytes = temp_file.read()

        os.unlink(temp_file.name)

        parent_metadata = [{**chunk.metadata, "page_content": chunk.page_content} for chunk in parent_chunks]
        parent_pkl_bytes = pickle.dumps(parent_metadata)

        logging.info(f"Parent index created. Vector shape: {parent_vectors.shape}")

        # Create and store child index
        child_vectors = np.array(embedding_function.embed_documents([chunk.page_content for chunk in child_chunks]), dtype=np.float32)
        child_index = faiss.IndexFlatL2(child_vectors.shape[1])
        child_index.add(child_vectors)

        # Serialize child index
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            faiss.write_index(child_index, temp_file.name)
            temp_file.seek(0)
            child_faiss_bytes = temp_file.read()

        os.unlink(temp_file.name)

        child_metadata = [{**chunk.metadata, "page_content": chunk.page_content} for chunk in child_chunks]
        child_pkl_bytes = pickle.dumps(child_metadata)

        logging.info(f"Child index created. Vector shape: {child_vectors.shape}")

        # Store in PostgreSQL
        db_helper.add_to_postgres_faiss(f"{directory_name}_parent", parent_faiss_bytes, parent_pkl_bytes)
        db_helper.add_to_postgres_faiss(f"{directory_name}_child", child_faiss_bytes, child_pkl_bytes)

        logging.info(f"FAISS indexes stored in PostgreSQL for {directory_name}")
        return "Success"
    except ex.DBFailureEx as e:
        logging.error(f"Database error in add_to_faiss: {e.detail}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in add_to_faiss: {str(e)}", exc_info=True)
        raise ex.APIException(
            status_code=500, msg="Unexpected error occurred", detail=f"Unexpected error in add_to_faiss: {str(e)}", code="5000001", ex=e
        )
