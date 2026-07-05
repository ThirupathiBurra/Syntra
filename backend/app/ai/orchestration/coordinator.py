from typing import Optional
from app.ai.models import ExecutionStatus
from .models import ExecutionContext
from app.core.logging import get_workflow_logger

logger = get_workflow_logger()

class ExecutionCoordinator:
    """
    Responsible for transitioning the state of the execution context.
    No actual AI execution logic exists here.
    """

    def __init__(self):
        # In a real implementation, this would connect to a state store
        pass

    def start(self, context: ExecutionContext) -> None:
        """Transitions workflow to RUNNING state."""
        context.status = ExecutionStatus.RUNNING
        logger.info("execution_started", f"Started execution for workflow {context.workflow_id}", {"workflow_id": context.workflow_id})

    def pause(self, context: ExecutionContext, reason: str = "") -> None:
        """Transitions workflow to PAUSED state (e.g. for approval)."""
        context.status = ExecutionStatus.PAUSED
        logger.info("execution_paused", f"Paused workflow {context.workflow_id}: {reason}", {"workflow_id": context.workflow_id, "reason": reason})

    def resume(self, context: ExecutionContext) -> None:
        """Transitions workflow back to RUNNING state."""
        context.status = ExecutionStatus.RUNNING
        logger.info("execution_resumed", f"Resumed workflow {context.workflow_id}", {"workflow_id": context.workflow_id})

    def cancel(self, context: ExecutionContext, reason: str = "") -> None:
        """Transitions workflow to CANCELLED state."""
        context.status = ExecutionStatus.CANCELLED
        logger.warning("execution_cancelled", f"Cancelled workflow {context.workflow_id}", {"workflow_id": context.workflow_id, "reason": reason})

    def complete(self, context: ExecutionContext) -> None:
        """Transitions workflow to COMPLETED state."""
        context.status = ExecutionStatus.COMPLETED
        logger.info("execution_completed", f"Completed workflow {context.workflow_id}", {"workflow_id": context.workflow_id})

    def fail(self, context: ExecutionContext, error: str) -> None:
        """Transitions workflow to FAILED state."""
        context.status = ExecutionStatus.FAILED
        logger.error("execution_failed", f"Workflow {context.workflow_id} failed", {"workflow_id": context.workflow_id, "error": error})
