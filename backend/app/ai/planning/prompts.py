from app.ai.providers.models import Prompt, PromptMessage
from typing import Any, Dict

def create_planner_prompt(
    user_request: str, 
    context: Dict[str, Any], 
    available_agents: list[str], 
    available_tools: list[str]
) -> Prompt:
    system_instruction = """
    You are the Chief Planning Engine for the Syntra Enterprise AI Platform.
    Your responsibility is to analyze the user's request and decompose it into a highly structured ExecutionPlan.
    
    CRITICAL RULES:
    1. Understand the intent. Break the work down into logical steps.
    2. Avoid hallucinations. Never assume capabilities that do not exist.
    3. ONLY use the registered agents provided in the context.
    4. ONLY use the registered tools provided in the context.
    5. Never invent new agents or tools.
    6. Return strictly valid JSON conforming to the ExecutionPlan schema.
    7. Assess the risk level. If external mutations (e.g., sending an email) are involved, human_approval_required MUST be true.
    """
    
    user_content = f"""
    USER REQUEST: {user_request}
    
    AVAILABLE AGENTS: {available_agents}
    
    AVAILABLE TOOLS: {available_tools}
    
    WORKFLOW CONTEXT: {context}
    
    Generate the ExecutionPlan JSON.
    """
    
    messages = [
        PromptMessage(role="system", content=system_instruction),
        PromptMessage(role="user", content=user_content)
    ]
    
    return Prompt(messages=messages, variables={}, metadata={"source": "planning_engine"})

def create_knowledge_requirement_prompt(user_request: str) -> Prompt:
    system_instruction = """
    You are the Knowledge Router for the Syntra Enterprise AI Platform.
    Analyze the user's request and determine if retrieving internal enterprise knowledge is necessary to fulfill it.
    If the request requires facts, documents, policies, past data, or context specific to the organization, return requires_knowledge=true.
    If it is a general request (e.g., "write a python script", "hello"), return requires_knowledge=false.
    If true, provide a concise search_query optimized for semantic vector search.
    """
    
    user_content = f"USER REQUEST: {user_request}\n\nDetermine knowledge requirement."
    
    messages = [
        PromptMessage(role="system", content=system_instruction),
        PromptMessage(role="user", content=user_content)
    ]
    
    return Prompt(messages=messages, variables={}, metadata={"source": "knowledge_router"})

