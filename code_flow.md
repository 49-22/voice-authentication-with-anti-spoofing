# Code Flow: Voice Authentication Enrollment

This document explains the code flow for the `/enroll` endpoint in the voice authentication system.

---

## 1. HTTP Request

- A client sends a `POST` request to the `/enroll` endpoint.
- The request typically contains user audio data or a precomputed embedding.

---

## 2. FastAPI Route Handler

- The `/enroll` endpoint is handled by the `enroll_user` function in `app/api_routes.py`.
- This function:
  - Processes the incoming request.
  - Extracts or computes the user's embedding.
  - Calls `save_to_faiss(user_id, embedding)` to store the embedding.

---

## 3. Saving to FAISS

- The `save_to_faiss` function (in `app/db_faiss.py`) is responsible for adding the user's embedding to the FAISS index.
- It expects:
  - The embedding to be a 2D numpy array of shape `(1, d)`.
  - The embedding's dimension `d` to match the FAISS index's dimension.

---

## 4. FAISS Index

- The FAISS index is used for fast similarity search of embeddings.
- The function `index.add(embedding)` adds the new embedding to the index.
- If the embedding's shape does not match the index's expected dimension, an `AssertionError` is raised.

---

## 5. Error Handling

- If an error occurs (such as a dimension mismatch), FastAPI returns a 500 Internal Server Error and logs the error.

---

## Summary Diagram

```
Client POST /enroll
        |
        v
FastAPI route: enroll_user()
        |
        v
save_to_faiss(user_id, embedding)
        |
        v
index.add(embedding)  <-- (Error if shape