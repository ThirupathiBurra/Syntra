from typing import Dict, List, Optional
from .models import AgentExecution

class RuntimeRegistry:
    """
    Maintains currently running agent executions.
    Supports lookup, cancellation, and monitoring.
    """
    def __init__(self):
        self._active_executions: Dict[str, AgentExecution] = {}

    def add(self, execution: AgentExecution) -> None:
        self._active_executions[execution.execution_id] = execution

    def remove(self, execution_id: str) -> None:
        if execution_id in self._active_executions:
            del self._active_executions[execution_id]

    def get(self, execution_id: str) -> Optional[AgentExecution]:
        return self._active_executions.get(execution_id)

    def list_active(self) -> List[AgentExecution]:
        return list(self._active_executions.values())

    def cancel(self, execution_id: str) -> bool:
        """Marks an execution for cancellation if active."""
        execution = self.get(execution_id)
        if execution:
            # Logic to signal cancellation to the running task would go here
            return True
        return False
