from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

class ExecutionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PAUSED = "PAUSED"
    CANCELLED = "CANCELLED"

class ApprovalState(str, Enum):
    NOT_REQUIRED = "NOT_REQUIRED"
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class AgentResult(BaseModel):
    agent_id: str
    status: ExecutionStatus
    output: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)

class Task(BaseModel):
    id: str
    workflow_id: str
    assigned_agent: str
    status: ExecutionStatus = ExecutionStatus.PENDING
    input_data: Dict[str, Any] = Field(default_factory=dict)
    result: Optional[AgentResult] = None
    approval_state: ApprovalState = ApprovalState.NOT_REQUIRED
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)

class Workflow(BaseModel):
    id: str
    name: str
    status: ExecutionStatus = ExecutionStatus.PENDING
    tasks: List[Task] = Field(default_factory=list)
    global_context: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)
