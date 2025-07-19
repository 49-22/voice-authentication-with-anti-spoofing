
# Project flow
+-------------+
|  User Voice |
+-------------+
      |
      v
+-------------------------+
| Frontend / CLI         |
| (Send voice via API)   |
+-------------------------+
      |
      v
+-------------------------+
| FastAPI Backend         |
+-------------------------+
|  /enroll      /verify   |
|  /spoof_check /challenge|
+-------------------------+
      |
      v
+------------------------------+
| Speaker Embedding Engine     |
| (ECAPA-TDNN - 512/192 vector)|
+------------------------------+
      |
      +--> Check Against Stored Embeddings (FAISS DB) (for a user)
      |
      +--> Pass to Anti-Spoofing Model (AASIST)
      |
      +--> Optionally pass to Whisper ASR for phrase verification
      |
      v
+--------------------------+
| Authentication Decision  |
+--------------------------+
      |
      v
+--------------------------+
| Return Auth Result (JSON)|
+--------------------------+