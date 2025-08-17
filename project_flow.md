
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
+---------------------------------------------------------------------------------------------------------------------+
| FastAPI Backend                                                                                                     |
+---------------------------------------------------------------------------------------------------------------------+
|  /enroll     (enroll with bot check as well)                                                                        |
|  /verify                                                                                                            |
|     /challenge/verify                   (this verifies the random text generated is matched or not)                 |
|     /spoof_check                        (this verifies if its not spoof voice)                                      |
      /closest-embedding-check            (this verifies if the user voice embedding is found)                        |
+---------------------------------------------------------------------------------------------------------------------+
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