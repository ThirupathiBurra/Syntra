from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime, timezone

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

class RuntimeState(str, Enum):
    IDLE = "IDLE"
    SCHEDULING = "SCHEDULING"
    EXECUTING = "EXECUTING"
    PAUSED = "PAUSED"
    SHUTTING_DOWN = "SHUTTING_DOWN"

class ExecutionStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class RetryPolicy(BaseModel):
    max_retries: int = 3
    backoff_factor: float = 2.0
    initial_delay_ms: int = 1000

class TimeoutPolicy(BaseModel):
    execution_timeout_ms: int = 30000
    connection_timeout_ms: int = 5000

class AgentExecution(BaseModel):
    execution_id: str
    agent_id: str
    workflow_id: str
    status: ExecutionStatus = ExecutionStatus.QUEUED
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    retry_policy: RetryPolicy = Field(default_factory=RetryPolicy)
    timeout_policy: TimeoutPolicy = Field(default_factory=TimeoutPolicy)
    attempt_count: int = 0
    created_at: datetime = Field(default_factory=now_utc)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class ExecutionQueue(BaseModel):
    items: List[AgentExecution] = Field(default_factory=list)
