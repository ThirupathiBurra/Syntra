from abc import ABC, abstractmethod
from typing import Any, Dict
from app.ai.compiler.models import CompiledWorkflow

class BaseExecutionStrategy(ABC):
    """Abstract strategy for executing a workflow graph."""
    
    @abstractmethod
    async def execute(self, workflow: CompiledWorkflow, session_id: str) -> Dict[str, Any]:
        pass

class SequentialExecutionStrategy(BaseExecutionStrategy):
    """Executes the graph one node at a time based on topological order."""
    async def execute(self, workflow: CompiledWorkflow, session_id: str) -> Dict[str, Any]:
        import asyncio
        from app.core.event_bus import event_bus
        from app.ai.execution.engine import execution_engine
        
        # 1. Topological Sort
        in_degree = {node_id: 0 for node_id in workflow.graph.nodes}
        for edge in workflow.graph.edges:
            in_degree[edge.target_id] += 1
            
        queue = [n for n, d in in_degree.items() if d == 0]
        sorted_nodes = []
        
        while queue:
            node_id = queue.pop(0)
            sorted_nodes.append(node_id)
            
            for edge in workflow.graph.edges:
                if edge.source_id == node_id:
                    in_degree[edge.target_id] -= 1
                    if in_degree[edge.target_id] == 0:
                        queue.append(edge.target_id)
                        
        if len(sorted_nodes) != len(workflow.graph.nodes):
            raise ValueError("Graph contains a cycle or unreachable nodes.")
            
        results = {}
        execution_context_data = {}
        
        # Extract original request from workflow description
        from app.workflows.composer.registry import workflow_registry
        from app.ai.agent_registry import agent_registry
        from app.services.document_generation.service import document_generation_service
        import logging
        
        logger = logging.getLogger(__name__)
        
        generated_wf = workflow_registry.get_workflow(workflow.workflow_id)
        original_request = generated_wf.description if generated_wf else "Perform general workflow task"
        
        # 2. Execute sequentially
        # Add slight initial delay to allow frontend SSE connection to establish (demo purposes)
        await asyncio.sleep(1.5)
        
        for node_id in sorted_nodes:
            node = workflow.graph.nodes[node_id]
            
            # Map agent_id to a human-readable node name for UI compatibility
            node_name = node.agent_id.replace("agent_", "").replace("_", " ").title()
            if node.agent_id == "agent_knowledge":
                node_name = "Knowledge Retrieval"
            elif node.agent_id == "agent_generation":
                node_name = "Document Generation"
            elif node.agent_id == "agent_system":
                node_name = "Human Approval"
            elif node.agent_id == "agent_comm":
                node_name = "Email Dispatch"
            elif node.agent_id == "agent_analysis":
                node_name = "Data Extraction"
                
            await event_bus.publish("NodeStarted", {"session_id": session_id, "node": node_name})
            
            output = {}
            try:
                # Real Execution Dispatch
                if node.agent_id == "agent_knowledge":
                    knowledge_agent = agent_registry.get("agent-knowledge-core")
                    agent_result = await knowledge_agent.execute({
                        "query": original_request,
                        "top_k": 5,
                        "workspace_id": "default",
                        "filters": {},
                        "min_confidence": 0.5
                    }, {})
                    output = agent_result.output
                    # Store raw context for downstream use
                    execution_context_data["knowledge_result"] = output.get("raw_context", "")
                    
                elif node.agent_id == "agent_generation":
                    context_text = execution_context_data.get("knowledge_result", "Standard default context.")
                    documents = await document_generation_service.generate_onboarding_package(context_text)
                    output = {"documents_generated": documents}
                    execution_context_data["generated_documents"] = documents
                    
                elif node.agent_id == "agent_system":
                    docs = execution_context_data.get("generated_documents", {})
                    await execution_engine.await_approval(session_id, {
                        "approval_type": "DYNAMIC_REVIEW",
                        "summary": docs.get("hr_summary", f"Review required for step: {node_name}"),
                        "generated_documents": docs
                    })
                    output = {"status": "WAITING_APPROVAL"}
                    
                elif node.agent_id == "agent_comm":
                    from app.core.logging import get_workflow_logger
                    workflow_logger = get_workflow_logger()
                    docs = execution_context_data.get("generated_documents", {})
                    email_body = docs.get("welcome_email", "Default welcome message.")
                    workflow_logger.info("email_dispatch", "Simulated sending email.", {"body": email_body[:50]})
                    output = {"status": "email_sent", "email_preview": email_body[:50]}
                    
                elif node.agent_id == "agent_analysis":
                    from app.ai.providers.manager import provider_manager
                    provider = provider_manager.get()
                    context_text = execution_context_data.get("knowledge_result", original_request)
                    prompt = f"Extract the top 3 key data points from the following text:\n{context_text}"
                    res = await provider.generate(prompt=prompt)
                    output = {"extracted_data": res.content}
                    execution_context_data["extracted_data"] = output["extracted_data"]

                else:
                    # Graceful fallback for unimplemented agents
                    logger.warning(f"Capability {node.agent_id} not fully implemented. Skipping.")
                    output = {"status": "success", "simulated": True, "note": "Graceful fallback"}
            
            except Exception as e:
                logger.error(f"Error executing node {node.agent_id}: {e}")
                output = {"status": "failed", "error": str(e)}
                
            # Simulated delay to show node in 'running' state in the UI
            await asyncio.sleep(1.5)
                
            await event_bus.publish("NodeCompleted", {"session_id": session_id, "node": node_name, "output": output})
            results[node_id] = output
            
            if output.get("status") == "WAITING_APPROVAL":
                # Halt sequential execution here, wait for human review to resume
                break
            
        has_approval = any(n.agent_id == "agent_system" for n in workflow.graph.nodes.values())
        return {
            "status": "WAITING_APPROVAL" if has_approval else "COMPLETED",
            "results": results
        }

class ParallelExecutionStrategy(BaseExecutionStrategy):
    """Executes independent nodes concurrently."""
    async def execute(self, workflow: CompiledWorkflow, session_id: str) -> Dict[str, Any]:
        # Architecture placeholder
        return {}

class LangGraphExecutionStrategy(BaseExecutionStrategy):
    """Future strategy that compiles internal graph to LangGraph."""
    async def execute(self, workflow: CompiledWorkflow, session_id: str) -> Dict[str, Any]:
        # Architecture placeholder
        return {}
