import logging
from typing import Dict, Any
from app.ai.orchestration.models import ExecutionContext
from app.knowledge.service import knowledge_service
from app.services.document_generation.service import document_generation_service
from app.ai.execution.engine import execution_engine
from app.core.event_bus import event_bus

logger = logging.getLogger(__name__)

class EmployeeOnboardingWorkflow:
    """
    Business workflow for AI Employee Copilot.
    Orchestrates Knowledge Retrieval -> Document Generation -> Human Approval.
    """
    
    async def execute(self, session_id: str, context: ExecutionContext) -> Dict[str, Any]:
        """
        Executes the onboarding business logic.
        In a fully integrated LangGraph setup, this would be represented as a DAG.
        Here we define the explicit steps.
        """
        try:
            # Step 1: Knowledge Retrieval
            await event_bus.publish("NodeStarted", {"session_id": session_id, "node": "Knowledge Retrieval"})
            knowledge_results = await knowledge_service.retrieve_context(
                query="employee onboarding compliance IT equipment",
                workspace_id="default"
            )
            
            # Combine retrieved text
            retrieved_text = "\n".join([chunk.text for chunk in knowledge_results])
            if not retrieved_text:
                retrieved_text = "Standard Corporate Onboarding Policy 2026. Standard equipment: MacBook Pro, Monitor. Standard week: Orientation Day 1, Technical Setup Day 2, Team Sync Day 3."
                
            await event_bus.publish("NodeCompleted", {"session_id": session_id, "node": "Knowledge Retrieval", "output": {"knowledge_chunks": len(knowledge_results)}})
            
            # Step 2: Document Generation
            await event_bus.publish("NodeStarted", {"session_id": session_id, "node": "Document Generation"})
            
            documents = await document_generation_service.generate_onboarding_package(retrieved_text)
            
            await event_bus.publish("NodeCompleted", {"session_id": session_id, "node": "Document Generation", "output": {"documents_generated": len(documents)}})
            
            # Step 3: Human Approval
            # The execution engine awaits approval, pausing the workflow.
            await execution_engine.await_approval(session_id, {
                "approval_type": "HR_REVIEW",
                "summary": documents["hr_summary"],
                "generated_documents": documents
            })
            
            return {
                "status": "WAITING_APPROVAL",
                "documents": documents
            }
            
        except Exception as e:
            logger.error(f"Error in EmployeeOnboardingWorkflow: {e}")
            await event_bus.publish("Error", {"session_id": session_id, "error": str(e)})
            raise e

employee_onboarding_workflow = EmployeeOnboardingWorkflow()
