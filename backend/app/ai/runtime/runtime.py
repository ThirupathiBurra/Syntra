from typing import Any, Dict
from app.core.logging import get_workflow_logger
from app.ai.agent_base import BaseAgent
from app.ai.orchestration.models import ExecutionContext
from app.ai.compiler.models import CompiledWorkflow
from app.ai.execution.engine import execution_engine
from .models import AgentExecution, ExecutionStatus
from .pipeline import ExecutionPipeline
from .registry import RuntimeRegistry
from .scheduler import BaseScheduler, SequentialScheduler

logger = get_workflow_logger()

class AgentRuntime:
    """
    The Agent Runtime layer.
    Executes, schedules, tracks, and manages AI agents.
    """
    def __init__(self, scheduler: BaseScheduler = None):
        self.scheduler = scheduler or SequentialScheduler()
        self.pipeline = ExecutionPipeline()
        self.registry = RuntimeRegistry()

    async def execute_agent(self, execution: AgentExecution, agent: BaseAgent, context: ExecutionContext) -> AgentExecution:
        """
        Coordinates the full lifecycle of a single agent execution.
        """
        self.registry.add(execution)
        execution.status = ExecutionStatus.RUNNING
        logger.info("runtime_agent_started", f"Agent {execution.agent_id} execution started", {"execution_id": execution.execution_id})

        success = False
        error = None
        try:
            await self.pipeline.prepare(execution, agent, context)
            
            is_valid = await self.pipeline.validate(execution, agent)
            if not is_valid:
                raise ValueError(f"Agent {execution.agent_id} input validation failed.")

            # Note: No actual AI logic here yet.
            result = await self.pipeline.execute(execution, agent, context)
            
            outputs = await self.pipeline.post_process(result, agent)
            execution.outputs = outputs
            execution.status = ExecutionStatus.COMPLETED
            success = True
            logger.info("runtime_agent_completed", f"Agent {execution.agent_id} execution completed", {"execution_id": execution.execution_id})

        except Exception as e:
            error = e
            execution.error = str(e)
            execution.status = ExecutionStatus.FAILED
            logger.error("runtime_agent_failed", f"Agent {execution.agent_id} execution failed", {"execution_id": execution.execution_id, "error": str(e)})

        finally:
            await self.pipeline.cleanup(execution, agent, success, error)
            self.registry.remove(execution.execution_id)

        return execution

    async def execute_workflow(self, workflow: CompiledWorkflow) -> Dict[str, Any]:
        """
        Delegates the compiled workflow execution to the Execution Engine.
        """
        logger.info("runtime_delegating_execution", "Delegating to Execution Engine", {"workflow_id": workflow.workflow_id})
        session = execution_engine.startup(workflow)
        return await execution_engine.execute(session.session_id, workflow)

# Singleton Runtime Instance
agent_runtime = AgentRuntime()
