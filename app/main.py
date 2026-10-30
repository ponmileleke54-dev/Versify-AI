from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from app.core.config import settings
from app.api.v1.endpoints import chat, audio, rag

# Initialize API router for v1 endpoints
api_router = APIRouter()
api_router.include_router(chat.router, prefix="/chat", tags=["Chat & AI Reasoning"])
api_router.include_router(audio.router, prefix="/audio", tags=["Audio Transcription"])
api_router.include_router(rag.router, prefix="/rag", tags=["Knowledge Base & RAG"])

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Enterprise-grade multi-faith and church automation AI backend for Versify."
)

# Configure CORS so your Tauri desktop app and web frontend can connect smoothly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows local requests from Tauri & web apps
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the v1 API router under the /api/v1 prefix
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Versify AI Backend",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)