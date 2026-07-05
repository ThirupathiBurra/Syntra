from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type
from pydantic import BaseModel
from .models import AgentResult, ExecutionStatus
from .tools import Tool
from .memory import BaseMemory

class AgentMetadata(BaseModel):
    id: str
    name: str
    description: str
    version: str = "1.0.0"

class BaseAgent(ABC):
    """
    Base class for all specialized AI Agents in Syntra.
    Defines the standard execution interface and lifecycle hooks.
    """
    
    def __init__(self, metadata: AgentMetadata):
        self.metadata = metadata
        self._tools: Dict[str, Tool] = {}
        self._memory_interfaces: Dict[str, BaseMemory] = {}

    def register_tool(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def register_memory(self, name: str, memory_layer: BaseMemory) -> None:
        self._memory_interfaces[name] = memory_layer

    def get_memory(self, name: str) -> BaseMemory:
        if name not in self._memory_interfaces:
            raise ValueError(f"Memory layer {name} not registered for agent {self.metadata.id}")
        return self._memory_interfaces[name]

    # Lifecycle Methods
    def on_start(self, context: Dict[str, Any]) -> None:
        """Hook called before execution begins."""
        pass

    def on_complete(self, result: AgentResult) -> None:
        """Hook called after execution succeeds."""
        pass

    def on_error(self, error: Exception) -> None:
        """Hook called when execution fails."""
        pass

    # Validation Hooks
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate input payload before execution."""
        return True

    def validate_outputs(self, outputs: Dict[str, Any]) -> bool:
        """Validate outputs before returning result."""
        return True

    # Core Execution
    @abstractmethod
    async def execute(self, inputs: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        The main execution loop for the agent.
        Must be implemented by subclasses.
        """
        pass
