from fastapi import APIRouter, UploadFile, File, Form
import uuid
import os
from app.speaker_model import extract_embedding
from app.db_faiss import save_to_faiss

router = APIRouter()

@router.post("/enroll")
async def enroll_user(file: UploadFile = File(...), user_id: str = Form(...), language: str = Form("en"), device: str = Form("unknown")):
    filename = f"temp_{uuid.uuid4()}.wav"

    with open(filename, "wb") as f:
        f.write(await file.read())

    embedding = extract_embedding(filename)
    os.remove(filename)

    save_to_faiss(user_id, embedding, language, device)

    return {"message": "User enrolled", "user_id": user_id}


# TODO: Verify

# TODO: Challenge

# TODO: Spoof detection / anti-spoofing

# view all enrolled users
@router.get("/users")
async def get_users():
    from app.db_faiss import load_faiss
    import pickle

    index = load_faiss()
    metadata_path = "data/embeddings/metadata.pkl"

    if not os.path.exists(metadata_path):
        return {"message": "No users enrolled"}

    with open(metadata_path, "rb") as f:
        metadata = pickle.load(f)

    users = []
    for idx in range(index.ntotal):
        user_id = metadata.get(idx, "Unknown")
        users.append({"index": idx, "user_id": user_id})

    return {"users": users}

@router.get("/user/{user_id}")
async def get_user(user_id: str):
    from app.db_faiss import get_user_metadata

    metadata = get_user_metadata(user_id)
    if not metadata:
        return {"message": "User not found"}

    return {"user_id": user_id, "metadata": metadata}