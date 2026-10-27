from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Enterprise-grade multi-faith and church automation AI backend for Versify."
)

# Configure CORS so your Tauri desktop app and web frontend can connect smoothly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your specific client domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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