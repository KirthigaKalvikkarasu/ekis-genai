# app/main.py

from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="EKIS AI System")

app.include_router(router)