from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from app.ai.models import ExecutionStatus, ApprovalState

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

class Priority(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ExecutionMode(str, Enum):
    SEQUENTIAL = "SEQUENTIAL"
    PARALLEL = "PARALLEL"

class PlanDependencies(BaseModel):
    depends_on: List[str] = Field(default_factory=list)
    wait_for_all: bool = True

class PlanStep(BaseModel):
    step_id: str
    description: str
    target_agent_id: Optional[str] = None
    priority: Priority = Priority.NORMAL
    dependencies: PlanDependencies = Field(default_factory=PlanDependencies)
    status: ExecutionStatus = ExecutionStatus.PENDING

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class ExecutionPlan(BaseModel):
    plan_id: str
    workflow_id: str
    goal: str = ""
    summary: str = ""
    reasoning_summary: str = ""
    execution_mode: ExecutionMode = ExecutionMode.SEQUENTIAL
    estimated_complexity: str = "LOW"
    estimated_steps: int = 0
    required_agents: List[str] = Field(default_factory=list)
    required_tools: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.LOW
    confidence_score: float = 0.0
    human_approval_required: bool = False
    execution_order: List[str] = Field(default_factory=list)
    steps: List[PlanStep] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=now_utc)

class ExecutionContext(BaseModel):
    """
    Strongly typed context object containing all state for a running workflow.
    """
    workflow_id: str
    user_id: str
    original_request: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)
    status: ExecutionStatus = ExecutionStatus.PENDING
    active_agents: List[str] = Field(default_factory=list)
    completed_tasks: List[str] = Field(default_factory=list)
    pending_tasks: List[str] = Field(default_factory=list)
    approval_status: ApprovalState = ApprovalState.NOT_REQUIRED
    plan: Optional[ExecutionPlan] = None
    compiled_workflow: Optional[Any] = None
