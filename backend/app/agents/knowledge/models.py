from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

class KnowledgeQuery(BaseModel):
    """The structured input for a knowledge search request."""
    query: str
    filters: Dict[str, Any] = Field(default_factory=dict)
    top_k: int = 5
    min_confidence: float = 0.5
    workspace_id: Optional[str] = None

class KnowledgeSource(BaseModel):
    """Metadata representing the origin of a piece of knowledge."""
    source_id: str
    source_type: str  # e.g., "document", "database", "slack"
    title: str
    url: Optional[str] = None
    author: Optional[str] = None
    created_at: Optional[datetime] = None
    last_modified_at: Optional[datetime] = None

class Citation(BaseModel):
    """A direct reference mapping extracted content to its source."""
    citation_id: str
    source: KnowledgeSource
    extracted_text: str
    relevance_score: float
    page_number: Optional[int] = None
    chunk_index: Optional[int] = None

class KnowledgeConfidence(BaseModel):
    """Metrics indicating the reliability of the retrieved results."""
    overall_score: float
    is_sufficient: bool
    missing_context_flags: List[str] = Field(default_factory=list)

class RetrievalMetadata(BaseModel):
    """Execution metadata for the retrieval process."""
    execution_time_ms: int
    total_sources_scanned: int
    total_chunks_matched: int
    query_expansion_used: bool = False

class KnowledgeResult(BaseModel):
    """The strict, final output of the Knowledge Agent."""
    query_id: str
    citations: List[Citation] = Field(default_factory=list)
    confidence: KnowledgeConfidence
    metadata: RetrievalMetadata
    raw_context: str = "" # Formatted context ready for downstream LLMs
