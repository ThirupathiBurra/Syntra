from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseMemory(ABC):
    """Base interface for all memory layers."""
    @abstractmethod
    def read(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def write(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

class SessionMemory(BaseMemory):
    """Memory spanning a single user interaction session."""
    pass

class WorkflowMemory(BaseMemory):
    """Persistent state memory for a specific long-running workflow."""
    pass

class UserMemory(BaseMemory):
    """Long-term memory storing user preferences and behavior across sessions."""
    pass

class KnowledgeMemory(ABC):
    """Interface for enterprise semantic knowledge retrieval (RAG)."""
    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def ingest(self, document: str, metadata: Dict[str, Any]) -> str:
        pass
