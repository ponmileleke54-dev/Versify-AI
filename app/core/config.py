import os
from dotenv import load_dotenv

# Load environment variables from .env file explicitly
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Versify AI Engine"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

settings = Settings()