from typing import BinaryIO, List, Dict, Any
import asyncio
from app.core.logging import get_workflow_logger
from app.ai.providers.manager import provider_registry
from .models import Document, UploadResponse
from .upload import UploadService
from .chunking import ChunkingService
from .repository import KnowledgeRepository
from .retriever import SemanticRetriever

logger = get_workflow_logger()

class KnowledgeService:
    """
    Orchestrates the complete RAG pipeline.
    Sits between the KnowledgeAgent and the underlying Repository/Retrievers.
    """
    
    def __init__(self):
        self.upload_service = UploadService()
        self.chunking_service = ChunkingService()
        self.repository = KnowledgeRepository()
        self.retriever = SemanticRetriever(self.repository)
        self.provider = provider_registry.get("gemini")

    async def ingest_file(self, file_stream: BinaryIO, filename: str, workspace_id: str, uploader_id: str) -> UploadResponse:
        """End-to-end ingestion pipeline."""
        # 1. Parse
        doc = await self.upload_service.process_upload(file_stream, filename, workspace_id, uploader_id)
        
        # 2. Chunk
        chunks = self.chunking_service.chunk(doc)
        doc.chunks = chunks
        
        # 3. Embed
        texts_to_embed = [c.content for c in chunks]
        if texts_to_embed:
            embeddings = await self.provider.embed(texts_to_embed, model_name="models/text-embedding-004")
            for chunk, emb in zip(chunks, embeddings):
                chunk.embedding = emb
                
        # 4. Store
        success = self.repository.ingest_document(doc)
        
        return UploadResponse(
            document_id=doc.document_id,
            status="COMPLETED" if success else "FAILED",
            chunks_processed=len(chunks),
            error=None if success else "Database ingestion failed"
        )

    async def retrieve_context(self, query: str, filters: Dict[str, Any], top_k: int = 5, min_confidence: float = 0.5) -> List[Dict[str, Any]]:
        """Delegates to the configured retriever."""
        return await self.retriever.retrieve(query, filters, top_k, min_confidence)

# Singleton
knowledge_service = KnowledgeService()
