from fastapi import APIRouter, UploadFile, File, Form
import uuid
import os
from app.speaker_model import extract_embedding
from app.db_faiss import save_to_faiss
from app.db_faiss import verify_speaker
from aasist.aasist_inference import infer_spoof_score
AASIST_CONFIG_PATH = "aasist/config/AASIST.conf"


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

@router.post("/verify")
async def verify_user(file: UploadFile = File(...)):
    filename = f"temp_verify.wav"
    with open(filename, "wb") as f:
        f.write(await file.read())
    
    embedding = extract_embedding(filename)
    os.remove(filename)

    result = verify_speaker(embedding)

    return result

@router.post("/spoof-check")
async def spoof_check(file: UploadFile = File(...)):
    # from app.spoof_detector import get_spoof_score
    # from aasist.config import AASISTConfig


    filename = f"temp_spoof.wav"
    with open(filename, "wb") as f:
        f.write(await file.read())
    
    # score = get_spoof_score(filename)
    score = infer_spoof_score(filename, AASIST_CONFIG_PATH, "aasist/models/weights/AASIST.pth")
    os.remove(filename)

    return {
        "liveness_score": round(score, 3),
        "verdict": "real" if score > 0.65 else "spoofed"
    }

@router.post("/delete-user/{user_id}")
async def delete_user(user_id: str):
    from app.db_faiss import delete_user

    success = delete_user(user_id)
    if not success:
        return {"message": "User not found or could not be deleted"}

    return {"message": "User deleted successfully"}