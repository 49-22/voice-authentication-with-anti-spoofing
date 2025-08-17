from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import uuid
import os
from app.speaker_model import extract_embedding
from app.db_faiss import save_to_faiss
from app.db_faiss import verify_speaker_embedding
from aasist.aasist_inference import infer_spoof_score
from app.asr_whisper import verify_phrase
from app.challenge import new_challenge, get_challenge, consume_challenge
AASIST_CONFIG_PATH = "aasist/config/AASIST.conf"


router = APIRouter()

@router.post("/enroll")
async def enroll_user(file: UploadFile = File(...), user_id: str = Form(...), language: str = Form("en"), device: str = Form("unknown"), expected_phrase: str = Form(None)):
    filename = f"temp_{uuid.uuid4()}.wav"

    with open(filename, "wb") as f:
        f.write(await file.read())

    if expected_phrase:
        ok, sim, said = verify_phrase(filename, expected_phrase, language=language, thresh=0.8)
        if not ok:
            os.remove(filename)
            return HTTPException(status_code=400, detail={"error": "passphrase_mismatch", "similarity": sim, "transcript": said})

    embedding = extract_embedding(filename)
    os.remove(filename)

    save_to_faiss(user_id, embedding, language, device)

    return {"message": "User enrolled", "user_id": user_id}


@router.post("/challenge/verify")
async def challenge_verify(challenge_id: str = Form(...), file: UploadFile = File(...)):
    meta = get_challenge(challenge_id)
    if not meta:
        raise HTTPException(status_code=400, detail="Challenge not found or expired")
    
    temp = f"temp_{uuid.uuid4()}.wav"

    with open(temp, "wb") as f:
        f.write(await file.read())

    ok, sim, said = verify_phrase(temp, meta["phrase"], langauge=meta["lang"], thresh=0.8)
    os.remove(temp)

    if not ok:
        return {"passphrase_ok": False, "similarity": sim, "transcript": said}
    
    consume_challenge(challenge_id)

    return {"passphrase_ok": True, "similarity": sim, "transcript": said, "expected": meta["phrase"]}

# TODO: Challenge
@router.get("/challenge/start")
def challenge_start(lang: str = "en"):
    cid, phrase, lang = new_challenge(lang)
    return {
        "challenge_id": cid,
        "phrase": phrase,
        "language": lang
    }

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
async def verify_user(file: UploadFile = File(...), expected_phrase: str = Form(None), language: str = Form(None)):
    filename = f"temp_{uuid.uuid4()}.wav"
    with open(filename, "wb") as f:
        f.write(await file.read())

    if expected_phrase:
        ok, sim, said = verify_phrase(filename, expected_phrase, langauge=language, thresh=0.8)
        if not ok:
            os.remove(filename)
            return {"status": "rejected", "reason": "passphrase_mismatch", "similarity": sim, "transcript": said}
    
    # TODO: Verify spoof-check before proceedig to embedding check, if failed, return here

    embedding = extract_embedding(filename)
    os.remove(filename)

    result = verify_speaker_embedding(embedding)

    if expected_phrase:
        result["passphrase_checked"] = True
        result["passphrase_similarity"] = round(sim, 3)
        result["transcript"] = said

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
