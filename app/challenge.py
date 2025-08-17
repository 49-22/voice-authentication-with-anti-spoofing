# Simple challenge generator (in-memory). For production use Redix.DB
import random
import string
from datetime import datetime, timedelta

CHALLENGES = {} # structure of the object: challenge_id -> {"phrasee": ..., "lang":..., "expires":...}

PHRASEES = {
    "en": [
        "The quick brown fox jumps over the lazy dog",
        "A journey of a thousand miles begins with a single step",
        "To be or not to be, that is the question",
        "All that glitters is not gold",
        "A picture is worth a thousand words",
    ],
    "hi": [
        "मैं बहुत खुश हूं",
        "आप कैसे हैं",
        "आज मौसम बहुत अच्छा है",
    ],
    "te": [
        "నేను చాలా సంతోషంగా ఉన్నాను",
        "మీరు ఎలా ఉన్నారు",
        "ఈ రోజు చాలా మంచి రోజు",
    ]
}

def _rand_id(n=9):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(n))

def new_challenge(lang: str = "en", ttl_sec: int = 1800):
    phrase = random.choice(PHRASEES.get(lang, PHRASEES["en"]))
    cid = _rand_id()
    CHALLENGES[cid] = {
        "phrase": phrase,
        "lang": lang,
        "expires": datetime.utcnow() + timedelta(seconds=ttl_sec)
    }
    return cid, phrase, lang

def get_challenge(cid: str):
    meta = CHALLENGES.get(cid)
    if not meta:
        return None
    if datetime.utcnow() > meta["expires"]:
        del CHALLENGES[cid]
        return None
    return meta

def consume_challenge(cid: str):
    return CHALLENGES.pop(cid, None)