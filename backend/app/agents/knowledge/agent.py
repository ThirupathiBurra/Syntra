import time
import uuid
from typing import Any, Dict, List

from app.core.logging import get_agent_logger
from app.core.errors import ValidationError
from app.ai.agent_base import BaseAgent, AgentMetadata
from app.ai.models import AgentResult, ExecutionStatus
from .models import (
    KnowledgeQuery, 
    KnowledgeResult, 
    Citation, 
    KnowledgeConfidence, 
    RetrievalMetadata,
    KnowledgeSource
)
from app.knowledge import knowledge_service

logger = get_agent_logger()

class KnowledgeAgent(BaseAgent):
    """
    Foundation for discovering and retrieving trusted knowledge.
    Does not generate answers or reason; strictly retrieves and structures context.
    """

    def __init__(self):
        metadata = AgentMetadata(
            id="agent-knowledge-core",
            name="Knowledge Retrieval Agent",
            description="Searches enterprise memory and returns structured, cited context.",
            version="1.0.0"
        )
        super().__init__(metadata)

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validates that the input contains a valid KnowledgeQuery schema."""
        try:
            KnowledgeQuery(**inputs)
            return True
        except Exception as e:
            logger.error("knowledge_validation_failed", "Input validation failed", {"error": str(e)})
            raise ValidationError(f"Invalid knowledge query: {str(e)}")

    async def search(self, query: KnowledgeQuery) -> List[Any]:
        """Executes a search via the KnowledgeService."""
        logger.info("knowledge_search_started", f"Searching for: {query.query}", {"query": query.query})
        
        # Prepare filters from the query
        filters = query.filters.copy()
        if query.workspace_id:
            filters["workspace_id"] = query.workspace_id
            
        results = await knowledge_service.retrieve_context(
            query=query.query,
            filters=filters,
            top_k=query.top_k,
            min_confidence=query.min_confidence
        )
        return results

    def retrieve(self, search_results: List[Any]) -> List[Citation]:
        """Maps Supabase RPC results into strictly typed Citations."""
        citations = []
        for result in search_results:
            source = KnowledgeSource(
                source_id=result.get("document_id", str(uuid.uuid4())),
                source_type="document",
                title=result.get("title", "Unknown Source")
            )
            citation = Citation(
                citation_id=f"cit-{uuid.uuid4().hex[:8]}",
                source=source,
                extracted_text=result.get("content", ""),
                relevance_score=result.get("similarity", 0.0),
                page_number=result.get("page_number", 1)
            )
            citations.append(citation)
        return citations

    def rank(self, citations: List[Citation], query: KnowledgeQuery) -> List[Citation]:
        """Placeholder for re-ranking results based on relevance score."""
        return citations

    def filter(self, citations: List[Citation], query: KnowledgeQuery) -> List[Citation]:
        """Placeholder for applying strict enterprise filters (e.g., min_confidence, RBAC)."""
        return [c for c in citations if c.relevance_score >= query.min_confidence]

    def validate_sources(self, citations: List[Citation]) -> bool:
        """Ensures all retrieved citations have valid sources to prevent hallucinations."""
        for citation in citations:
            if not citation.source or not citation.source.source_id:
                return False
        return True

    def prepare_context(self, citations: List[Citation]) -> str:
        """Formats the validated citations into a context string for downstream agents."""
        return "\n\n".join([f"[{c.citation_id}] {c.extracted_text}" for c in citations])

    async def execute(self, inputs: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        The core execution lifecycle of the Knowledge Agent.
        Uses the internal pipeline methods to guarantee structure.
        """
        start_time = time.time()
        
        # 1. Parse and Validate
        query = KnowledgeQuery(**inputs)
        
        # 2. Search & Retrieve
        raw_results = await self.search(query)
        unfiltered_citations = self.retrieve(raw_results)
        
        # 3. Filter & Rank
        filtered_citations = self.filter(unfiltered_citations, query)
        ranked_citations = self.rank(filtered_citations, query)
        
        # 4. Validate sources for absolute trust
        if not self.validate_sources(ranked_citations):
            logger.error("knowledge_validation_failed", "Source validation failed for retrieved context.")
            raise ValidationError("Retrieved context contained untraceable sources.")
            
        logger.info("knowledge_sources_found", f"Found {len(ranked_citations)} valid sources.")

        # 5. Format Output
        formatted_context = self.prepare_context(ranked_citations)
        
        # 6. Calculate Confidence
        # Placeholder confidence logic
        confidence = KnowledgeConfidence(
            overall_score=0.95 if ranked_citations else 0.0,
            is_sufficient=len(ranked_citations) > 0,
            missing_context_flags=[] if ranked_citations else ["NO_MATCHES_FOUND"]
        )
        logger.info("knowledge_confidence_calculated", f"Confidence: {confidence.overall_score}")

        # 7. Construct Metadata
        exec_time = int((time.time() - start_time) * 1000)
        metadata = RetrievalMetadata(
            execution_time_ms=exec_time,
            total_sources_scanned=len(raw_results),
            total_chunks_matched=len(ranked_citations)
        )

        # 8. Final Result
        final_result = KnowledgeResult(
            query_id=f"q-{uuid.uuid4().hex[:8]}",
            citations=ranked_citations,
            confidence=confidence,
            metadata=metadata,
            raw_context=formatted_context
        )

        return AgentResult(
            agent_id=self.metadata.id,
            status=ExecutionStatus.COMPLETED,
            output=final_result.model_dump(mode="json"),
            metrics={"execution_time_ms": exec_time}
        )

# Instantiate the agent
knowledge_agent = KnowledgeAgent()
