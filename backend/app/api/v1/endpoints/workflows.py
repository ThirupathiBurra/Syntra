from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

from app.ai.orchestration.conductor import syntra_conductor
from app.ai.orchestration.models import ExecutionContext
from app.ai.compiler.models import CompiledWorkflow

from app.ai.execution.engine import execution_engine
from app.ai.compiler.models import CompiledWorkflow
from app.workflows.employee_onboarding.workflow import employee_onboarding_workflow
from app.workflows.composer.registry import workflow_registry

router = APIRouter()

@router.get("")
async def list_workflows():
    """List all generated workflows."""
    return workflow_registry.list_workflows()

class WorkflowCreateRequest(BaseModel):
    user_id: str
    request: str
    metadata: Optional[Dict[str, Any]] = None

async def run_workflow_bg(session_id: str, context: ExecutionContext):
    # In a real system, the ExecutionEngine would compile the ExecutionPlan into a CompiledWorkflow and run it.
    # For Milestone 13, we wire the specific EmployeeOnboardingWorkflow directly to demonstrate business logic.
    try:
        await employee_onboarding_workflow.execute(session_id, context)
    except Exception as e:
        print(f"Workflow background execution failed: {e}")

@router.post("", response_model=ExecutionContext)
async def create_workflow(request: WorkflowCreateRequest, background_tasks: BackgroundTasks):
    """
    Initialize a new workflow execution session.
    """
    try:
        context = await syntra_conductor.initialize(
            user_id=request.user_id,
            request=request.request,
            metadata=request.metadata or {}
        )
        
        # We start up the Execution Engine
        dummy_compiled = CompiledWorkflow(workflow_id=context.workflow_id, nodes={}, entry_node_id="", dependencies={})
        session = execution_engine.startup(dummy_compiled)
        
        background_tasks.add_task(run_workflow_bg, session.session_id, context)
        
        return context
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
async def generate_workflow(request: WorkflowCreateRequest):
    """
    Dynamically compose a new workflow from a natural language request.
    """
    from app.workflows.composer.engine import workflow_composer
    from app.workflows.composer.registry import workflow_registry
    try:
        workflow = await workflow_composer.compose(request.request)
        workflow_registry.save_workflow(workflow)
        return workflow
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{workflow_id}/execute")
async def execute_generated_workflow(workflow_id: str, background_tasks: BackgroundTasks):
    """
    Execute a previously generated workflow dynamically.
    """
    from app.workflows.composer.registry import workflow_registry
    from app.ai.orchestration.models import ExecutionPlan, PlanStep, PlanDependencies
    from app.ai.compiler.compiler import execution_compiler
    
    try:
        # 1. Fetch GeneratedWorkflow from registry
        generated_wf = workflow_registry.get_workflow(workflow_id)
        if not generated_wf:
            raise ValueError(f"Workflow {workflow_id} not found in registry.")
            
        # 2. Translate GeneratedWorkflow to ExecutionPlan
        steps = []
        for node in generated_wf.nodes:
            deps = generated_wf.dependencies.get(node.node_id, [])
            step = PlanStep(
                step_id=node.node_id,
                description=node.description,
                dependencies=PlanDependencies(depends_on=deps)
            )
            cap = workflow_registry.get_capability(node.capability_id)
            if cap:
                step.target_agent_id = cap.agent_id
            steps.append(step)
            
        plan = ExecutionPlan(
            plan_id=f"plan_{workflow_id}",
            workflow_id=workflow_id,
            steps=steps
        )
        
        # 3. Compile the plan into a CompiledWorkflow DAG
        compiled_workflow = execution_compiler.compile(plan)
        
        # 4. Trigger the real dynamic execution engine
        session = execution_engine.startup(compiled_workflow)
        background_tasks.add_task(execution_engine.execute, session.session_id, compiled_workflow)
        
        return {"session_id": session.session_id}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str):
    """
    Retrieve a generated workflow by ID.
    """
    workflow = workflow_registry.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.get("/{workflow_id}/graph")
async def get_workflow_graph(workflow_id: str):
    """
    Retrieve the compiled execution graph for the workflow (DAG).
    """
    raise HTTPException(status_code=501, detail="Persistence layer not fully wired in mock yet.")
