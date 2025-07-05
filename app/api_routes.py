from fastapi import APIRouter, UploadFile, File, Form
import uuid
import os
from app.speaker_model import extract_embedding
from app.db_faiss import save_to_faiss

router = APIRouter()

@router.post("/enroll")
async def enroll_user(file: UploadFile = File(...), user_id: str = Form(...)):
    filename = f"temp_{uuid.uuid4()}.wav"

    with open(filename, "Wb") as f:
        f.write(await file.read())

    embedding = extract_embedding(filename)
    os.remove(filename)

    save_to_faiss(user_id, embedding)

    return {"message": "User enrolled", "user_id": user_id}