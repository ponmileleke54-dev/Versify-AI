import os
from typing import Dict, List, Optional
from openai import OpenAI
from app.core.config import settings

class LLMService:
    def __init__(self):
        # Initializes OpenAI or alternative model clients using configured settings
        self.api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def get_system_prompt(self, mode: str) -> str:
        """
        Dynamically returns system instructions based on the request context.
        """
        prompts = {
            "general": (
                "You are an elite, highly intelligent AI assistant equipped with universal knowledge across science, "
                "academics, humanities, culture, and technology. Provide accurate, clear, and professional answers."
            ),
            "multi_faith": (
                "You are an expert scholar in Comparative World Religions and Theology, profoundly knowledgeable across "
                "Christianity, Islam, Hinduism, Buddhism, Sikhism, Judaism, and other faith traditions. Answer with theological "
                "rigor, historical accuracy, textual precision, and respectful scholarly neutrality. Cite primary scriptures where applicable."
            ),
            "sermon_prep": (
                "You are a deeply equipped Christian AI assistant with exhaustive knowledge of the Bible (all translations), "
                "Hebrew/Greek original terms, commentaries, church history, and systematic theology. Assist pastors with sermon outlines, "
                "exegetical insights, contextual cross-references, and practical applications."
            ),
            "church_media": (
                "You are an automated church service and media director AI inside Versify. Assist with lyrics identification, "
                "slide creation, worship sequence coordination, and real-time order-of-service management."
            )
        }
        return prompts.get(mode, prompts["general"])

    async def generate_response(
        self, 
        prompt: str, 
        mode: str = "general", 
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generates a completion from the LLM given a prompt, mode, and optional chat history.
        """
        if not self.client:
            return "API Key is missing. Please set your OPENAI_API_KEY in the .env file."

        messages = [{"role": "system", "content": self.get_system_prompt(mode)}]
        
        if chat_history:
            messages.extend(chat_history)
            
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Can be configured or mapped to open-source alternatives
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error connecting to LLM service: {str(e)}"

# Singleton instance for easy import across endpoints
llm_service = LLMService()