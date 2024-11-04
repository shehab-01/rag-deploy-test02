import hashlib
import numpy as np


def get_safe_path(directory_name):
    hash_object = hashlib.md5(directory_name.encode())
    safe_name = hash_object.hexdigest()
    safe_name = directory_name
    return f"D:\\Rag_vectorDB\\faiss_{safe_name}"


def convert_to_json_serializable(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_to_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    else:
        return obj
