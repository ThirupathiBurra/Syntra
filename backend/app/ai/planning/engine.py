import uuid
from typing import Any, Dict

from app.ai.providers.manager import provider_registry
from app.ai.providers.models import ModelConfig, GenerationConfig, SafetyConfig, RetryConfig, TimeoutConfig
from app.ai.orchestration.models import ExecutionPlan, ExecutionContext
from app.ai.agent_registry import agent_registry
from app.core.logging import get_workflow_logger
from app.core.errors import AIError

from .prompts import create_planner_prompt
from .validator import PlanValidator

logger = get_workflow_logger()
from pydantic import BaseModel
from app.agents.knowledge.agent import KnowledgeAgent

class KnowledgeRequirement(BaseModel):
    requires_knowledge: bool
    search_query: str = ""

class Planner:
    """Core logic for calling the AI Provider to generate a plan."""
    
    async def generate_plan(self, context: ExecutionContext, available_agents: list[str], available_tools: list[str]) -> ExecutionPlan:
        from .prompts import create_planner_prompt
        prompt = create_planner_prompt(
            user_request=context.original_request,
            context=context.metadata,
            available_agents=available_agents,
            available_tools=available_tools
        )
        
        provider = provider_registry.get("gemini")
        model_config = ModelConfig(model_name="gemini-2.5-flash", temperature=0.1)
        gen_config = GenerationConfig(json_mode=True)
        safety_config = SafetyConfig()
        retry_config = RetryConfig()
        timeout_config = TimeoutConfig()
        
        logger.info("planner_generation_started", "Requesting plan from Gemini", {"workflow_id": context.workflow_id})
        
        try:
            response = await provider.generate_structured(
                prompt=prompt,
                schema=ExecutionPlan,
                model_config=model_config,
                gen_config=gen_config,
                safety_config=safety_config,
                retry_config=retry_config,
                timeout_config=timeout_config
            )
            
            plan_data = response.structured_data
            if not plan_data:
                raise AIError("Provider returned empty structured data.")
                
            plan_data["plan_id"] = f"plan-{uuid.uuid4().hex[:8]}"
            plan_data["workflow_id"] = context.workflow_id
            
            return ExecutionPlan(**plan_data)
            
        except Exception as e:
            logger.error("planner_generation_failed", str(e))
            raise AIError(f"Failed to generate plan: {str(e)}")

class PlanningStrategy:
    """Defines different strategies for planning (e.g., fast, deep reasoning)."""
    pass

class PlanningService:
    """
    Coordinates the planner and validator.
    Called by the Conductor.
    """
    def __init__(self):
        self.planner = Planner()
        
    async def determine_knowledge_requirement(self, request: str) -> KnowledgeRequirement:
        from .prompts import create_knowledge_requirement_prompt
        prompt = create_knowledge_requirement_prompt(request)
        provider = provider_registry.get("gemini")
        
        model_config = ModelConfig(model_name="gemini-2.5-flash", temperature=0.0)
        gen_config = GenerationConfig(json_mode=True)
        
        response = await provider.generate_structured(
            prompt=prompt,
            schema=KnowledgeRequirement,
            model_config=model_config,
            gen_config=gen_config,
            safety_config=SafetyConfig(),
            retry_config=RetryConfig(),
            timeout_config=TimeoutConfig()
        )
        
        if not response.structured_data:
            return KnowledgeRequirement(requires_knowledge=False)
        return KnowledgeRequirement(**response.structured_data)
        
    async def create_plan(self, context: ExecutionContext) -> ExecutionPlan:
        # Step 1: Conditional Retrieval (RAG)
        req = await self.determine_knowledge_requirement(context.original_request)
        if req.requires_knowledge and req.search_query:
            logger.info("planner_rag_triggered", f"Query: {req.search_query}")
            agent = KnowledgeAgent()
            # Execute Knowledge Agent
            knowledge_result = await agent.execute({
                "query": req.search_query,
                "top_k": 5
            })
            # Inject context
            context.metadata["enterprise_knowledge"] = knowledge_result

        # Step 2: Full Plan Generation
        registered_agents = [metadata.id for metadata in agent_registry.list_metadata()]
        registered_tools = ["search_tool", "sql_tool"]
        
        validator = PlanValidator(registered_agents, registered_tools)
        plan = await self.planner.generate_plan(context, registered_agents, registered_tools)
        validator.validate(plan)
        
        logger.info("plan_created_and_validated", "Successfully created execution plan", {"plan_id": plan.plan_id})
        return plan

# Singleton
planning_service = PlanningService()

