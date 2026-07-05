from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel

class ToolParameters(BaseModel):
    """Base class for defining tool input schemas."""
    pass

class Tool(ABC):
    """
    Generic Tool Interface.
    Every tool must define its name, description, and strongly-typed input schema.
    """
    name: str
    description: str
    schema_cls: type[ToolParameters]

    @abstractmethod
    def execute(self, params: ToolParameters, context: Dict[str, Any]) -> Any:
        """Executes the tool with the provided parameters and contextual state."""
        pass
