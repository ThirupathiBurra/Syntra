from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class ExecutionStage(str, Enum):
    PREPARATION = "PREPARATION"
    EXECUTION = "EXECUTION"
    VALIDATION = "VALIDATION"
    CLEANUP = "CLEANUP"

class NodeMetadata(BaseModel):
    estimated_duration_ms: int = 0
    retry_allowed: bool = True
    timeout_ms: int = 30000

class ExecutionMetadata(BaseModel):
    compiled_at: str
    total_nodes: int
    total_edges: int
    is_parallelizable: bool = False

class CompiledNode(BaseModel):
    node_id: str
    agent_id: str
    stage: ExecutionStage = ExecutionStage.EXECUTION
    dependencies: List[str] = Field(default_factory=list)
    metadata: NodeMetadata = Field(default_factory=NodeMetadata)
    payload_template: Dict[str, Any] = Field(default_factory=dict)

class CompiledEdge(BaseModel):
    source_id: str
    target_id: str
    condition: Optional[str] = None

class ExecutionGraph(BaseModel):
    nodes: Dict[str, CompiledNode] = Field(default_factory=dict)
    edges: List[CompiledEdge] = Field(default_factory=list)
    entry_nodes: List[str] = Field(default_factory=list)

class CompiledWorkflow(BaseModel):
    workflow_id: str
    plan_id: str
    graph: ExecutionGraph = Field(default_factory=ExecutionGraph)
    metadata: ExecutionMetadata
