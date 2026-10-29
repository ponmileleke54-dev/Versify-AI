from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from app.services.llm_service import llm_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    mode: Optional[str] = "general"  # Options: 'general', 'multi_faith', 'sermon_prep', 'church_media'
    history: Optional[List[Dict[str, str]]] = []

class ChatResponse(BaseModel):
    response: str
    mode_used: str

@router.post("/completions", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
        
    ai_response = await llm_service.generate_response(
        prompt=request.message,
        mode=request.mode,
        chat_history=request.history
    )
    
    return ChatResponse(
        response=ai_response,
        mode_used=request.mode
    )