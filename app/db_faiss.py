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

def verify_speaker_embedding(query_embedding, threshold=0.75):
    index = faiss.read_index(index_path)
    query_embedding = np.array([query_embedding]).astype('float32')

    # Search for top 1 most similar vector embedding
    D, I = index.search(query_embedding, k=1) # D is distances, I is indices

    with open(meta_path, "rb") as f:
        metadata = pickle.load(f)
    
    top_index = int(I[0][0])
    distance = D[0][0]
    similarity = 1 - distance  # Convert distance to similarity (cosisne similarity)

    user_info = metadata.get(top_index, {"user_id": "Unknown"})
    if similarity >= threshold:
        return {
            "status": "autheticated",
            "user_id": user_info["user_id"],
            "similarity": round(similarity, 3),

        }
    else:
        return {
            "status": "unauthenticated",
            "similarity": round(similarity, 3),
        }

def delete_user(user_id):
    index = load_faiss()
    if index.ntotal == 0:
        return "No users enrolled"

    with open(meta_path, "rb") as f:
        metadata = pickle.load(f)

    # Find the index of the user_id
    user_index = None
    for idx, info in metadata.items():
        # info can be user_id or other metadata
        # Check if user_id matches
        if isinstance(info, dict) and "user_id" in info:
            if info["user_id"] == user_id:
                user_index = int(idx)
                break
        elif isinstance(info, str) and info == user_id:
            user_index = int(idx)
            break
    
    if user_index is None:
        return "User not found"

    # Remove the user from the index
    index.remove_ids(np.array([user_index], dtype=np.int64))
    faiss.write_index(index, index_path)

    # Remove metadata entry
    del metadata[user_index]

    with open(meta_path, "wb") as f:
        pickle.dump(metadata, f)

    return f"User {user_id} deleted successfully"