import os
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
from app.core.config import settings
from app.core.logging import get_workflow_logger
from .models import Document, DocumentChunk

logger = get_workflow_logger()

class KnowledgeRepository:
    """Handles interactions with Supabase pgvector."""
    
    def __init__(self):
        url = settings.SUPABASE_URL or ""
        key = settings.SUPABASE_KEY or ""
        self.client: Optional[Client] = None
        
        if url and key:
            try:
                self.client = create_client(url, key)
            except Exception as e:
                logger.warning("supabase_init_failed", str(e))

    def ingest_document(self, document: Document) -> bool:
        """Inserts document metadata and chunks into Supabase."""
        if not self.client:
            logger.warning("supabase_not_configured", "Mocking document ingestion.")
            return True
            
        try:
            # 1. Insert Document
            doc_data = {
                "id": document.document_id,
                "workspace_id": document.metadata.workspace_id,
                "title": document.metadata.title,
                "department": document.metadata.department,
                "document_type": document.metadata.document_type,
                "owner": document.metadata.owner,
                "created_at": document.metadata.created_at.isoformat(),
            }
            self.client.table("documents").insert(doc_data).execute()
            
            # 2. Insert Chunks
            chunk_data = []
            for chunk in document.chunks:
                chunk_data.append({
                    "id": chunk.chunk_id,
                    "document_id": chunk.document_id,
                    "content": chunk.content,
                    "page_number": chunk.page_number,
                    "embedding": chunk.embedding,
                    "metadata": chunk.metadata
                })
            self.client.table("document_chunks").insert(chunk_data).execute()
            return True
        except Exception as e:
            logger.error("supabase_ingest_failed", str(e))
            return False

    def search_similar(self, query_embedding: List[float], workspace_id: str, limit: int = 5, min_confidence: float = 0.5) -> List[Dict[str, Any]]:
        """Performs a pgvector similarity search via Supabase RPC."""
        if not self.client:
            logger.warning("supabase_not_configured", "Mocking similarity search.")
            return []
            
        try:
            # Assumes an RPC function `match_document_chunks` exists in Supabase
            response = self.client.rpc(
                "match_document_chunks",
                {
                    "query_embedding": query_embedding,
                    "match_threshold": min_confidence,
                    "match_count": limit,
                    "filter_workspace_id": workspace_id
                }
            ).execute()
            return response.data
        except Exception as e:
            logger.error("supabase_search_failed", str(e))
            return []

    def delete_document(self, document_id: str, workspace_id: str) -> bool:
        if not self.client:
            return True
        try:
            self.client.table("documents").delete().eq("id", document_id).eq("workspace_id", workspace_id).execute()
            return True
        except Exception as e:
            logger.error("supabase_delete_failed", str(e))
            return False
