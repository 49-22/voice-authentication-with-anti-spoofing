import faiss
import numpy as np
import os
import pickle
from datetime import datetime

index_path = "data/embeddings/faiss.index"
meta_path = "data/embeddings/metadata.pkl"

# initialize index of FAISS
def load_faiss():
    if os.path.exists(index_path):
        return faiss.read_index(index_path)
    else:
        return faiss.IndexFlatL2(192)  # temporarily Changed from 512 to 192

# save embedding to FAISS
def save_to_faiss(user_id, embedding, language="en", device="unknown", model="ECAPA-TDNN"):
    index = load_faiss()
    # Ensure embedding is a 2D float32 numpy array
    embedding = np.asarray(embedding, dtype=np.float32)

    # TODO: error handling for embedding shape
    if embedding.ndim == 1:
        embedding = embedding.reshape(1, -1)
    assert embedding.shape[1] == index.d, f"Embedding dim {embedding.shape[1]} != index dim {index.d}"
    
    index.add(embedding)
    faiss.write_index(index, index_path)

    metadata = {}
    if os.path.exists(meta_path):
        with open(meta_path, "rb") as f:
            metadata = pickle.load(f)
    else:
        metadata = {}
    
    entry = {
        "user_id": user_id,
        language: language,
        "device_info": device,
        "embedding_model": model,
        "enrollment_time": datetime.now().isoformat(),
        # Add other metadata fields as needed  
    }

    metadata[index.ntotal - 1] = entry

    # TODO: Add remaining metadata handling like device, language, model used, purpose, liveness_score, timestamp etc.

    with open(meta_path, "wb") as f:
        pickle.dump(metadata, f)
        f"Saved metadata for user {user_id} at index {index.ntotal - 1}"

def get_user_metadata(user_id):
    if not os.path.exists(meta_path):
        return None
    
    with open(meta_path, "rb") as f:
        metadata = pickle.load(f)
    
    for idx, uid in metadata.items():
        if uid == user_id:
            return metadata[idx]
    
    return None