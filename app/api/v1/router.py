from fastapi import APIRouter
from app.api.v1.endpoints import chat, audio, rag

api_router = APIRouter()
api_router.include_router(chat.router, prefix="/chat", tags=["Chat & AI Reasoning"])
api_router.include_router(audio.router, prefix="/audio", tags=["Live Audio & Worship Automation"])
api_router.include_router(rag.router, prefix="/rag", tags=["Multi-Faith RAG & Vector Knowledge"])