# voice-authentication-with-anti-spoofing
Voice-Based Biometric Authentication with Multilingual and Anti-spoofing capabilities


To run this repo, follow the setup as follows:
# install core depdencies
1. pip install fastapi uvicorn pydantic numpy scipy
2. pip install torch torchaudio
3. pip install faiss-cpu
4. pip install speechbrain
5. pip install librosa  // Python library used for analyzing and extracting features from audio and music signals.

# Anti-spoofing model
1. git clone https://github.com/clovaai/aasist 
2. cd aasist && pip install -r requirements.txt
3. git submodule https://github.com/clovaai/aasist aasist // This generates a file with this link to other called ".gitmodules"

# to start server
1. uvicorn app.main:app --reload

# To enroll
5. curl -X POST http://localhost:8000/enroll \
  -F "user_id=test_user" \
  -F "file=@app/voice/common_voice_en_41910500.mp3"

# To fetch a single user
6. curl -X GET http://localhost:8000/users/test_user1

# To fetch all users
7. curl -X GET http://localhost:8000/users/

# To verify
curl -X POST http://localhost:8000/verify \
  -F "file=@app/voice/common_voice_en_41910500.mp3"

# To Spoof check
curl -X POST http://localhost:8000/spoof-check \
  -F "file=@app/voice/common_voice_en_41910500.mp3"

<!-- Dataset -->
<!-- Challenges -->
<!-- has been done so-far with screenshots and voice -->