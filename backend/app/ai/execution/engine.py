import uuid
from typing import Dict, Any, Optional
from app.core.logging import get_workflow_logger
from app.ai.compiler.models import CompiledWorkflow
from .models import ExecutionSession, ExecutionSnapshot, ExecutionProgress
from .strategy import BaseExecutionStrategy, SequentialExecutionStrategy

logger = get_workflow_logger()

class ExecutionEngine:
    """
    Responsible for executing CompiledWorkflow objects.
    Coordinates graph traversal, node scheduling, pausing, and resuming.
    """
    
    def __init__(self, default_strategy: BaseExecutionStrategy = None):
        self.strategy = default_strategy or SequentialExecutionStrategy()
        self._active_sessions: Dict[str, ExecutionSession] = {}

    def startup(self, workflow: CompiledWorkflow) -> ExecutionSession:
        session_id = f"exec-{uuid.uuid4().hex[:8]}"
        session = ExecutionSession(session_id=session_id, workflow_id=workflow.workflow_id)
        self._active_sessions[session_id] = session
        logger.info("execution_started", "ExecutionEngine started workflow", {"session_id": session_id})
        return session

    async def execute(self, session_id: str, workflow: CompiledWorkflow) -> Dict[str, Any]:
        """Main execution loop abstraction."""
        if session_id not in self._active_sessions:
            raise ValueError(f"Session {session_id} not found.")
            
        session = self._active_sessions[session_id]
        session.status = "RUNNING"
        
        # Delegates to strategy (which may use LangGraphAdapter in the future)
        result = await self.strategy.execute(workflow, session_id)
        
        self.complete(session_id)
        return result

    def pause(self, session_id: str) -> None:
        if session_id in self._active_sessions:
            self._active_sessions[session_id].status = "PAUSED"
            self.checkpoint(session_id)
            logger.info("execution_paused", "Execution paused", {"session_id": session_id})

    async def await_approval(self, session_id: str, context_data: dict) -> None:
        if session_id in self._active_sessions:
            self._active_sessions[session_id].status = "WAITING_APPROVAL"
            self.checkpoint(session_id)
            logger.info("approval_requested", "Execution waiting for human approval", {"session_id": session_id})
            
            # If the event_bus is available, publish the event
            try:
                from app.core.event_bus import event_bus
                await event_bus.publish("ApprovalRequested", {
                    "session_id": session_id,
                    "status": "WAITING_APPROVAL",
                    **context_data
                })
            except Exception as e:
                logger.error(f"Failed to publish ApprovalRequested event: {e}")

    def resume(self, session_id: str) -> None:
        if session_id in self._active_sessions:
            self._active_sessions[session_id].status = "RUNNING"
            logger.info("execution_resumed", "Execution resumed", {"session_id": session_id})

    def cancel(self, session_id: str) -> None:
        if session_id in self._active_sessions:
            self._active_sessions[session_id].status = "CANCELLED"
            logger.info("execution_cancelled", "Execution cancelled", {"session_id": session_id})

    def complete(self, session_id: str) -> None:
        if session_id in self._active_sessions:
            self._active_sessions[session_id].status = "COMPLETED"
            logger.info("execution_completed", "Execution completed", {"session_id": session_id})

    def checkpoint(self, session_id: str) -> None:
        """Persists execution state."""
        # Architecture placeholder
        pass
        
    def get_snapshot(self, session_id: str) -> Optional[ExecutionSnapshot]:
        session = self._active_sessions.get(session_id)
        if not session:
            return None
        return ExecutionSnapshot(
            session_id=session.session_id,
            status=session.status,
            cursor=session.cursor,
            progress=ExecutionProgress(), # Placeholder calc
            nodes=session.nodes
        )

# Singleton
execution_engine = ExecutionEngine()
