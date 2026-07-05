from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

class NodeExecution(BaseModel):
    node_id: str
    status: str = "PENDING"
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    outputs: Dict[str, Any] = Field(default_factory=dict)

class ExecutionCursor(BaseModel):
    current_node_ids: List[str] = Field(default_factory=list)
    completed_node_ids: List[str] = Field(default_factory=list)

class ExecutionProgress(BaseModel):
    total_nodes: int = 0
    completed_nodes: int = 0
    failed_nodes: int = 0
    percent_complete: float = 0.0

class WorkflowCheckpoint(BaseModel):
    checkpoint_id: str
    workflow_id: str
    state_data: Dict[str, Any]
    created_at: datetime = Field(default_factory=now_utc)

class ExecutionSnapshot(BaseModel):
    session_id: str
    status: str
    cursor: ExecutionCursor
    progress: ExecutionProgress
    nodes: Dict[str, NodeExecution] = Field(default_factory=dict)

class ExecutionSession(BaseModel):
    session_id: str
    workflow_id: str
    status: str = "INITIALIZED"
    cursor: ExecutionCursor = Field(default_factory=ExecutionCursor)
    nodes: Dict[str, NodeExecution] = Field(default_factory=dict)
    started_at: Optional[datetime] = None
    updated_at: datetime = Field(default_factory=now_utc)
