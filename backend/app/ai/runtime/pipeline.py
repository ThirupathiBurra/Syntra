from typing import Any, Dict
from app.ai.agent_base import BaseAgent
from app.ai.orchestration.models import ExecutionContext
from .models import AgentExecution

class ExecutionPipeline:
    """
    Reusable execution pipeline for standardizing agent execution lifecycle.
    """

    async def prepare(self, execution: AgentExecution, agent: BaseAgent, context: ExecutionContext) -> None:
        """Initializes state, loads memory, and triggers agent on_start hook."""
        agent.on_start(context.model_dump())

    async def validate(self, execution: AgentExecution, agent: BaseAgent) -> bool:
        """Validates agent inputs before execution."""
        return agent.validate_inputs(execution.inputs)

    async def execute(self, execution: AgentExecution, agent: BaseAgent, context: ExecutionContext) -> Any:
        """Core execution block where the actual AI logic will run."""
        # This will be replaced by actual logic calling agent.execute()
        return {}

    async def post_process(self, result: Any, agent: BaseAgent) -> Dict[str, Any]:
        """Validates outputs and formats the result."""
        # Assume result is a dict for now
        outputs = result if isinstance(result, dict) else {}
        agent.validate_outputs(outputs)
        return outputs

    async def cleanup(self, execution: AgentExecution, agent: BaseAgent, success: bool, error: Exception = None) -> None:
        """Cleans up resources and triggers appropriate completion/error hooks."""
        if success:
            # agent.on_complete(...) would be called here
            pass
        else:
            if error:
                agent.on_error(error)
