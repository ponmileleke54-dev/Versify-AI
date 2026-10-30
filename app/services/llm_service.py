import os
from openai import OpenAI
from app.core.config import settings
from app.services.rag_service import rag_service

class LLMService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def _get_system_prompt(self, mode: str, rag_context: str = "") -> str:
        base_prompts = {
            "general": "You are Versify AI, a professional desktop assistant designed for enterprise workflows and multi-faith scholarship.",
            "sermon_prep": "You are an elite theological research partner and sermon preparation assistant. Provide deep scriptural insights, exegesis, structural sermon outlines, and cross-references.",
            "multi_faith": "You are an objective comparative theology scholar. Compare religious texts with historical accuracy, respect, and academic rigour.",
            "church_media": "You are an expert Church Media Director. Format responses into clean presentation slides, lower-thirds, and visual production cues."
        }
        
        prompt = base_prompts.get(mode, base_prompts["general"])
        if rag_context:
            prompt += f"\n\n[RELEVANT VERIFIED KNOWLEDGE/SCRIPTURE]:\n{rag_context}\n\nUse the above context to answer accurately where applicable."
        return prompt

    async def generate_response(self, message: str = None, prompt: str = None, mode: str = "general", history: list = None, **kwargs) -> str:
        if not self.client:
            return "Error: OpenAI API Key missing in backend configuration."

        # Handle parameter alias for callers passing either 'message' or 'prompt'
        query_text = message or prompt or ""

        rag_context = ""
        # Automatically pull vector storage context for study modes
        if mode in ["sermon_prep", "multi_faith"]:
            namespace = "christian_bible" if mode == "sermon_prep" else "general_knowledge"
            try:
                matches = rag_service.search_knowledge_base(namespace=namespace, query=query_text, k=3)
                if matches:
                    rag_context = "\n---\n".join([m["content"] for m in matches])
            except Exception as e:
                # Log or ignore vector search errors gracefully so chat doesn't break if DB is empty
                print(f"RAG search warning: {str(e)}")

        system_prompt = self._get_system_prompt(mode, rag_context)

        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": query_text})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error communicating with AI engine: {str(e)}"

llm_service = LLMService()