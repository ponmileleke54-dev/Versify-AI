import shutil
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.audio_service import audio_service

router = APIRouter()

TEMP_DIR = "temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)

@router.post("/transcribe-worship")
async def transcribe_worship_audio(file: UploadFile = File(...)):
    """
    Receives a live audio recording chunk from the desktop app,
    transcribes it using Whisper, and matches it to worship lyrics.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No audio file provided.")

    file_path = os.path.join(TEMP_DIR, file.filename)
    
    try:
        # Save uploaded audio file chunk locally temporarily
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Transcribe using Whisper
        transcript = await audio_service.transcribe_audio_chunk(file_path)
        
        # Match against song lyrics database for presentation auto-advance
        match_result = audio_service.match_worship_song(transcript)

        return {
            "status": "success",
            "transcription": transcript,
            "presentation_action": match_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio processing failed: {str(e)}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)