from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.core.logging import get_workflow_logger
from app.ai.providers.manager import provider_registry
from .repository import KnowledgeRepository

logger = get_workflow_logger()

class BaseRetriever(ABC):
    """Abstract interface for retrieving knowledge."""
    @abstractmethod
    async def retrieve(self, query: str, filters: Dict[str, Any], top_k: int, min_confidence: float) -> List[Dict[str, Any]]:
        pass

class SemanticRetriever(BaseRetriever):
    """Retrieves context using vector embeddings."""
    
    def __init__(self, repository: KnowledgeRepository):
        self.repository = repository
        self.provider = provider_registry.get("gemini")

    async def retrieve(self, query: str, filters: Dict[str, Any], top_k: int, min_confidence: float) -> List[Dict[str, Any]]:
        logger.info("semantic_retrieval_started", "Generating query embedding")
        
        # 1. Embed query using Provider Layer (No direct Gemini SDK import)
        embeddings = await self.provider.embed([query], model_name="models/text-embedding-004")
        query_embedding = embeddings[0]
        
        # 2. Search Repository
        workspace_id = filters.get("workspace_id", "default")
        results = self.repository.search_similar(query_embedding, workspace_id, top_k, min_confidence)
        
        return results

# Future: HybridRetriever(BaseRetriever) combining Semantic and BM25
