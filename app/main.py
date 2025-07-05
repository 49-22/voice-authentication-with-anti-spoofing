from fastapi import FastAPI
from app.api_routes import router

app = FastAPI()
app.include_router(router)

