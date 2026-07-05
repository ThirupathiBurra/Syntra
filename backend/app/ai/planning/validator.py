from typing import List
from app.ai.orchestration.models import ExecutionPlan
from app.core.errors import ValidationError
from app.core.logging import get_workflow_logger

logger = get_workflow_logger()

class PlanValidator:
    """Validates generated execution plans for safety and correctness."""
    
    def __init__(self, available_agents: List[str], available_tools: List[str]):
        self.available_agents = set(available_agents)
        self.available_tools = set(available_tools)

    def validate(self, plan: ExecutionPlan) -> bool:
        try:
            self._check_agents(plan.required_agents)
            self._check_tools(plan.required_tools)
            self._check_circular_dependencies(plan)
            return True
        except ValidationError as e:
            logger.error("plan_validation_failed", str(e), {"plan_id": plan.plan_id})
            raise

    def _check_agents(self, required_agents: List[str]) -> None:
        for agent in required_agents:
            if agent not in self.available_agents:
                raise ValidationError(f"Plan references unknown agent: {agent}")

    def _check_tools(self, required_tools: List[str]) -> None:
        for tool in required_tools:
            if tool not in self.available_tools:
                raise ValidationError(f"Plan references unknown tool: {tool}")

    def _check_circular_dependencies(self, plan: ExecutionPlan) -> None:
        # Placeholder for a topological sort check
        pass
