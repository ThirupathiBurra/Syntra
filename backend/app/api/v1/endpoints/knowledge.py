from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Dict, Any

from app.knowledge.service import knowledge_service
from app.core.config import get_supabase_client

router = APIRouter()

@router.get("")
async def list_documents():
    """List all documents."""
    supabase = get_supabase_client()
    if not supabase:
        return []
    try:
        response = supabase.table("documents").select("*").order("created_at", desc=True).execute()
        # Map Supabase DB rows to the frontend-expected schema
        mapped_data = []
        for row in response.data:
            mapped_data.append({
                "document_id": row.get("id"),
                "name": row.get("title"),
                "type": row.get("document_type"),
                "owner": row.get("owner"),
                "size": "Unknown", # Not stored currently
                "status": "Indexed", # Vectorized
                "created_at": row.get("created_at")
            })
        return mapped_data
    except Exception as e:
        print(f"Failed to fetch documents: {e}")
        return []

class KnowledgeSearchRequest(BaseModel):
    query: str
    workspace_id: str
    limit: int = 5
    min_score: float = 0.7

@router.post("/search")
async def search_knowledge(request: KnowledgeSearchRequest):
    """
    Search the enterprise knowledge base.
    """
    try:
        results = await knowledge_service.retrieve_context(
            query=request.query,
            workspace_id=request.workspace_id,
            limit=request.limit,
            min_score=request.min_score
        )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    workspace_id: str = Form("default-workspace"),
    uploader_id: str = Form("demo-user")
):
    """
    Upload a document, chunk it, embed it via Gemini, and store in Supabase pgvector.
    """
    try:
        response = await knowledge_service.ingest_file(
            file_stream=file.file,
            filename=file.filename,
            workspace_id=workspace_id,
            uploader_id=uploader_id
        )
        return response
    except Exception as e:
        print(f"Failed to ingest document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

