# voice-authentication-with-anti-spoofing
Voice-Based Biometric Authentication with Multilingual and Anti-spoofing capabilities


To run this repo, follow the setup as follows:
# install core depdencies
1. pip install fastapi uvicorn pydantic numpy scipy
2. pip install torch torchaudio
3. pip install faiss-cpu
4. pip install speechbrain
5. pip install librosa  // Python library used for analyzing and extracting features from audio and music signals.
6. install faster-whisper
7. install whisper-jax for faster inference 
  pip install git+https://github.com/sanchit-gandhi/whisper-jax.git
  pip install --upgrade "jax[cpu]"  # cpu installation of jax
8. vasista22/whisper-telugu-base 



# Anti-spoofing model
1. git clone https://github.com/clovaai/aasist 
2. cd aasist && pip install -r requirements.txt
3. git submodule https://github.com/clovaai/aasist aasist // This generates a file with this link to other called ".gitmodules"

# Active speech recognition
1. faster-whiser
2. vasista22/whisper-telugu-base for telugu

# to start server
1. uvicorn app.main:app --reload

# To enroll
5. curl -X POST http://localhost:8000/enroll \
  -F "user_id=test_user" \
  -F "file=@app/voice/common_voice_en_41910500.mp3"

# To enroll with a phrase
curl -X POST http://localhost:8000/enroll \
  -F "user_id=test_user" \
  -F "file=@app/voice/common_voice_en_41910500.mp3"
  -F "expected_phrase="To be or not to be, that is the question"

# To fetch a single user
6. curl -X GET http://localhost:8000/users/test_user1

# To fetch all users
7. curl -X GET http://localhost:8000/users/

# Generate a challenge phrase and verify with your voice
## Generate
curl -X GET http://localhost:8000/challenge/start <!-- This generates a challenge_id and picked phrase in language.
curl -X GET http://localhost:8000/challenge/start?lang=te <!-- This generates a challenge_id and picked phrase in telugu.

## verify the challenge with a voice print of mine
curl -X POST http://localhost:8000/challenge/verify \
  -F "challenge_id=BtiI2j4Tk" \
  -F "file=@app/voice/Nitin_Telugu.mp3"

# To verify (phrase check -> anti-spoof check -> find the user in the DB)
curl -X POST http://localhost:8000/verify \
  -F "file=@app/voice/common_voice_en_41910500.mp3"

# To Spoof check
curl -X POST http://localhost:8000/spoof-check \
  -F "file=@app/voice/common_voice_en_41910500.mp3"
