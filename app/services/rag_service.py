import os
from typing import List, Dict, Any
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings

class RAGService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key) if self.api_key else None
        self.persist_directory = "./chroma_db"
        
    def get_vector_store(self, collection_name: str = "general_knowledge"):
        """
        Initializes or loads a local ChromaDB collection (namespace) for specific domains.
        """
        if not self.embeddings:
            raise ValueError("OpenAI API key is missing for embeddings generation.")
            
        return Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

    def add_documents_to_namespace(self, namespace: str, texts: List[str], metadatas: List[Dict[str, Any]] = None):
        """
        Ingests texts (e.g., Bible verses, commentaries, comparative texts) into a specific namespace.
        """
        vector_store = self.get_vector_store(collection_name=namespace)
        vector_store.add_texts(texts=texts, metadatas=metadatas)
        vector_store.persist()
        return {"status": "success", "added_count": len(texts), "namespace": namespace}

    def search_knowledge_base(self, namespace: str, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Searches the specified vector namespace for context matching the user's query.
        """
        try:
            vector_store = self.get_vector_store(collection_name=namespace)
            results = vector_store.similarity_search_with_score(query, k=k)
            
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "relevance_score": float(score)
                })
            return formatted_results
        except Exception as e:
            # Fallback if collection doesn't exist yet or DB is empty
            return []

rag_service = RAGService()