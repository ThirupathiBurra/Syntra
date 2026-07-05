from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Any, Dict, Optional

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

class BaseEvent(BaseModel):
    event_id: str
    timestamp: datetime = Field(default_factory=now_utc)
    workflow_id: str

class WorkflowStarted(BaseEvent):
    event_type: str = "WorkflowStarted"
    initial_context: Dict[str, Any]

class TaskStarted(BaseEvent):
    event_type: str = "TaskStarted"
    task_id: str
    agent_id: str

class TaskCompleted(BaseEvent):
    event_type: str = "TaskCompleted"
    task_id: str
    agent_id: str
    result: Dict[str, Any]

class TaskFailed(BaseEvent):
    event_type: str = "TaskFailed"
    task_id: str
    agent_id: str
    error_message: str

class ApprovalRequested(BaseEvent):
    event_type: str = "ApprovalRequested"
    task_id: str
    agent_id: str
    proposed_action: Dict[str, Any]

class WorkflowCompleted(BaseEvent):
    event_type: str = "WorkflowCompleted"
    final_output: Dict[str, Any]

# --- Runtime Events ---

class AgentQueued(BaseEvent):
    event_type: str = "AgentQueued"
    execution_id: str
    agent_id: str

class AgentStarted(BaseEvent):
    event_type: str = "AgentStarted"
    execution_id: str
    agent_id: str

class AgentFinished(BaseEvent):
    event_type: str = "AgentFinished"
    execution_id: str
    agent_id: str
    outputs: Dict[str, Any]

class AgentFailed(BaseEvent):
    event_type: str = "AgentFailed"
    execution_id: str
    agent_id: str
    error: str

class AgentCancelled(BaseEvent):
    event_type: str = "AgentCancelled"
    execution_id: str
    agent_id: str

# --- Execution Engine Events ---

class WorkflowExecutionStarted(BaseEvent):
    event_type: str = "WorkflowExecutionStarted"
    session_id: str
    workflow_id: str

class NodeStarted(BaseEvent):
    event_type: str = "NodeStarted"
    session_id: str
    node_id: str

class NodeCompleted(BaseEvent):
    event_type: str = "NodeCompleted"
    session_id: str
    node_id: str
    outputs: Dict[str, Any]

class NodeSkipped(BaseEvent):
    event_type: str = "NodeSkipped"
    session_id: str
    node_id: str
    reason: str

class NodeFailed(BaseEvent):
    event_type: str = "NodeFailed"
    session_id: str
    node_id: str
    error: str

class WorkflowPaused(BaseEvent):
    event_type: str = "WorkflowPaused"
    session_id: str

class WorkflowResumed(BaseEvent):
    event_type: str = "WorkflowResumed"
    session_id: str

class WorkflowFinished(BaseEvent):
    event_type: str = "WorkflowFinished"
    session_id: str
    workflow_id: str
    status: str


