from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

class DocumentMetadata(BaseModel):
    title: str
    workspace_id: str
    department: str = "general"
    document_type: str = "unknown" # e.g., "pdf", "csv", "docx"
    owner: str = "system"
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)
    embedding_version: str = "1.0.0"

class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    page_number: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    embedding: Optional[List[float]] = None

class Document(BaseModel):
    document_id: str
    content: str # full raw content
    metadata: DocumentMetadata
    chunks: List[DocumentChunk] = Field(default_factory=list)

class UploadResponse(BaseModel):
    document_id: str
    status: str
    chunks_processed: int
    error: Optional[str] = None
