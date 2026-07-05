from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from app.ai.planning.engine import planning_service
from app.ai.orchestration.models import ExecutionPlan

router = APIRouter()

class PlanningPreviewRequest(BaseModel):
    request: str
    user_id: str
    context: Dict[str, Any] = {}

@router.post("/preview", response_model=ExecutionPlan)
async def preview_plan(request: PlanningPreviewRequest):
    """
    Generate an ExecutionPlan without actually initializing a workflow.
    Useful for showing the user what will happen before they commit.
    """
    try:
        plan = await planning_service.create_plan(
            request=request.request,
            context=request.context
        )
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
