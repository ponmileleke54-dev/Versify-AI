import os
from openai import OpenAI
from app.core.config import settings

class AudioService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    async def transcribe_audio_chunk(self, file_path: str) -> str:
        """
        Transcribes an audio chunk file (mp3, wav, webm) using OpenAI Whisper API.
        """
        if not self.client:
            return "Error: OpenAI API key is missing for audio transcription."

        try:
            with open(file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return transcript
        except Exception as e:
            return f"Error processing audio transcription: {str(e)}"

    def match_worship_song(self, transcribed_text: str) -> dict:
        """
        Smart matcher to map live transcribed lyrics/speech to known church hymns 
        or worship songs and determine the exact slide/verse.
        """
        # Placeholder mock logic for matching lyrics against a song database
        cleaned_text = transcribed_text.strip().lower()
        
        # In the upcoming builds, we will query our song library vector space here
        return {
            "matched_song": "Amazing Grace",
            "current_verse": "Verse 1: Amazing grace! how sweet the sound",
            "confidence_score": 0.92,
            "raw_transcript": cleaned_text
        }

audio_service = AudioService()