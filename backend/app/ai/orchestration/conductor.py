import uuid
from typing import Any, Dict
from datetime import datetime, timezone

from app.core.logging import get_workflow_logger
from app.ai.events import (
    WorkflowStarted, 
    WorkflowCompleted,
    TaskFailed
)
from app.ai.models import ExecutionStatus
from .models import ExecutionContext, ExecutionPlan
from .coordinator import ExecutionCoordinator
from .aggregator import ResultAggregator
from app.ai.planning.engine import planning_service
from app.ai.compiler import execution_compiler
from app.ai.runtime.runtime import agent_runtime

logger = get_workflow_logger()

class Conductor:
    """
    The central intelligence of Syntra.
    Coordinates workflow lifecycle, plans execution, and manages agents.
    """
    
    def __init__(self):
        self.coordinator = ExecutionCoordinator()
        self.aggregator = ResultAggregator()
        self.is_healthy = True

    async def initialize(self, request: str, user_id: str, metadata: Dict[str, Any] = None) -> ExecutionContext:
        """
        Creates the initial execution context and generates a plan.
        """
        context = ExecutionContext(
            workflow_id=f"wf-{uuid.uuid4().hex[:8]}",
            user_id=user_id,
            original_request=request,
            metadata=metadata or {}
        )
        
        logger.info("workflow_initialized", "Initialized new workflow", {"workflow_id": context.workflow_id})
        
        # 1. Generate execution plan via AI Planning Engine
        plan = await self.plan(context)
        context.plan = plan
        
        # 2. Compile the execution plan into a workflow graph
        compiled_workflow = execution_compiler.compile(plan)
        context.compiled_workflow = compiled_workflow
        
        return context

    async def plan(self, context: ExecutionContext) -> ExecutionPlan:
        """
        Delegates to the AI Planning Engine to dynamically create an execution plan based on the user's request.
        """
        logger.info("workflow_planning_started", "Generating AI Execution Plan", {"workflow_id": context.workflow_id})
        
        # Call the Planning Engine (which calls Gemini via ProviderManager)
        plan = await planning_service.create_plan(context)
        
        logger.info("workflow_planning_completed", "Execution Plan Generated", {"plan_id": plan.plan_id})
        return plan

    def execute(self, context: ExecutionContext) -> None:
        """
        Starts the workflow execution and coordinates agents.
        Publishes WorkflowStarted event.
        """
        self.coordinator.start(context)
        
        # Publish event
        event = WorkflowStarted(
            event_id=f"evt-{uuid.uuid4().hex[:8]}",
            workflow_id=context.workflow_id,
            initial_context={"request": context.original_request}
        )
        logger.info("workflow_event_published", "WorkflowStarted", {"event": event.model_dump(mode="json")})
        
        # Delegate to Agent Runtime (Placeholder structure)
        # Note: Actual iteration over tasks and agent lookup will happen here.
        # agent_runtime.execute_agent(execution_params...)

    def validate(self, context: ExecutionContext) -> bool:
        """
        Validates the current state of execution.
        Uses the aggregator to check for conflicts in completed agent results.
        """
        merged_data = self.aggregator.merge_results()
        return self.aggregator.validate_hooks(merged_data)

    def complete(self, context: ExecutionContext) -> Dict[str, Any]:
        """
        Finalizes execution and aggregates results.
        Publishes WorkflowCompleted event.
        """
        self.coordinator.complete(context)
        final_output = self.aggregator.merge_results()
        
        event = WorkflowCompleted(
            event_id=f"evt-{uuid.uuid4().hex[:8]}",
            workflow_id=context.workflow_id,
            final_output=final_output
        )
        logger.info("workflow_event_published", "WorkflowCompleted", {"event": event.model_dump(mode="json")})
        return final_output

    def fail(self, context: ExecutionContext, error_msg: str) -> None:
        """
        Handles critical failures in the workflow.
        """
        self.coordinator.fail(context, error_msg)
        
        event = TaskFailed(
            event_id=f"evt-{uuid.uuid4().hex[:8]}",
            workflow_id=context.workflow_id,
            task_id="global",
            agent_id="conductor",
            error_message=error_msg
        )
        logger.error("workflow_event_published", "WorkflowFailed", {"event": event.model_dump(mode="json")})

# Singleton instance
syntra_conductor = Conductor()
