import faiss
import numpy as np
import os
import pickle

index_path = "data/embeddings/faiss.index"
meta_path = "data/embeddings/metadata.pkl"

# initialize index of FAISS
def load_faiss():
    if os.path.exists(index_path):
        return faiss.read_index(index_path)
    else:
        return faiss.IndexFlatL2(192)  # Changed from 512 to 192

# save embedding to FAISS
def save_to_faiss(user_id, embedding):
    index = load_faiss()
    # Ensure embedding is a 2D float32 numpy array
    embedding = np.asarray(embedding, dtype=np.float32)
    if embedding.ndim == 1:
        embedding = embedding.reshape(1, -1)
    assert embedding.shape[1] == index.d, f"Embedding dim {embedding.shape[1]} != index dim {index.d}"
    
    index.add(embedding)
    faiss.write_index(index, index_path)

    metadata = {}
    if os.path.exists(meta_path):
        with open(meta_path, "rb") as f:
            metadata = pickle.load(f)
    metadata[index.ntotal - 1] = user_id

    with open(meta_path, "wb") as f:
        pickle.dump(metadata, f)