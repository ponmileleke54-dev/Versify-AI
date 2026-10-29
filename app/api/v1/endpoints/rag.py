from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.services.rag_service import rag_service

router = APIRouter()

class IngestRequest(BaseModel):
    namespace: str  # e.g., 'christian_bible', 'islamic_texts', 'general_knowledge'
    texts: List[str]
    metadatas: Optional[List[Dict[str, Any]]] = None

class QueryRAGRequest(BaseModel):
    namespace: str
    query: str
    k: Optional[int] = 3

@router.post("/ingest")
def ingest_data(request: IngestRequest):
    """
    Ingests raw text documents/scriptures into a specific multi-faith or general vector namespace.
    """
    try:
        result = rag_service.add_documents_to_namespace(
            namespace=request.namespace,
            texts=request.texts,
            metadatas=request.metadatas
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
def query_rag(request: QueryRAGRequest):
    """
    Queries a specific vector namespace to retrieve contextual text citations.
    """
    try:
        results = rag_service.search_knowledge_base(
            namespace=request.namespace,
            query=request.query,
            k=request.k
        )
        return {
            "namespace": request.namespace,
            "query": request.query,
            "matches": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))