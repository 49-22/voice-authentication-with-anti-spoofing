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
        return faiss.IndexFlatL2(512)

# save embedding to FAISS
def save_to_faiss(user_id, embedding):
    index = load_faiss()
    embedding = np.array([embedding]).astype("float32")
    index.add(embedding)
    faiss.write_index(index, index_path)

    metadata = {}
    if os.path.exists(meta_path):
        with open(meta_path, "rb") as f:
            metadata = pickle.load(f)
    metadata[index.ntotal - 1] = user_id

    with open(meta_path, "wb") as f:
        pickle.dump(metadata, f)