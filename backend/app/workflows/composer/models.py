from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

def generate_uuid() -> str:
    return uuid.uuid4().hex

class WorkflowCapability(BaseModel):
    id: str
    name: str
    description: str
    agent_id: str
    requires_approval: bool = False

class GeneratedNode(BaseModel):
    node_id: str
    capability_id: str
    description: str
    reasoning: str  # Explainability: why this was chosen

class GeneratedWorkflow(BaseModel):
    workflow_id: str = Field(default_factory=generate_uuid)
    name: str
    description: str
    department: str = "General"
    tags: List[str] = Field(default_factory=list)
    
    nodes: List[GeneratedNode]
    dependencies: Dict[str, List[str]]
    
    # Explainability & Readiness
    confidence: float
    estimated_duration: str
    estimated_cost: str
    risks: List[str] = Field(default_factory=list)
    requires_human_approval: bool
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    version: int = 1
    execution_count: int = 0
