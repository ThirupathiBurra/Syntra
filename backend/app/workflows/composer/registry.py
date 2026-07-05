from typing import List, Optional
from .models import WorkflowCapability, GeneratedWorkflow
from app.core.config import get_supabase_client

class WorkflowRegistry:
    def __init__(self):
        self.supabase = get_supabase_client()
        self._memory_workflows = {}
        # Hardcoded for Milestone 15 as requested: available generic capabilities
        self.capabilities = [
            WorkflowCapability(id="cap_knowledge_retrieval", name="Knowledge Retrieval", description="Search enterprise knowledge base", agent_id="agent_knowledge"),
            WorkflowCapability(id="cap_doc_generation", name="Document Generation", description="Generate formatted documents using LLMs", agent_id="agent_generation"),
            WorkflowCapability(id="cap_human_approval", name="Human Approval", description="Pause execution for explicit human review", agent_id="agent_system", requires_approval=True),
            WorkflowCapability(id="cap_email_dispatch", name="Email Dispatch", description="Send automated emails", agent_id="agent_comm"),
            WorkflowCapability(id="cap_data_extraction", name="Data Extraction", description="Extract structured data from unstructured text", agent_id="agent_analysis"),
        ]

    def get_capabilities(self) -> List[WorkflowCapability]:
        return self.capabilities

    def get_capability(self, cap_id: str) -> Optional[WorkflowCapability]:
        for cap in self.capabilities:
            if cap.id == cap_id:
                return cap
        return None

    def save_workflow(self, workflow: GeneratedWorkflow) -> None:
        self._memory_workflows[workflow.workflow_id] = workflow
        if not self.supabase:
            print("Supabase client not configured. Skipping persistence.")
            return
            
        data = workflow.dict()
        data['created_at'] = data['created_at'].isoformat()
        try:
            self.supabase.table("workflows").insert(data).execute()
        except Exception as e:
            print(f"Failed to save workflow to Supabase (using memory fallback): {e}")

    def list_workflows(self) -> List[dict]:
        if not self.supabase:
            return [w.dict() for w in self._memory_workflows.values()]
        try:
            response = self.supabase.table("workflows").select("*").order("created_at", desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Failed to fetch workflows from Supabase (using memory fallback): {e}")
            return [w.dict() for w in self._memory_workflows.values()]

    def get_workflow(self, workflow_id: str) -> Optional[GeneratedWorkflow]:
        if not self.supabase:
            return self._memory_workflows.get(workflow_id)
        try:
            response = self.supabase.table("workflows").select("*").eq("workflow_id", workflow_id).execute()
            if response.data:
                return GeneratedWorkflow(**response.data[0])
            return self._memory_workflows.get(workflow_id)
        except Exception as e:
            print(f"Failed to fetch workflow {workflow_id} from Supabase (using memory fallback): {e}")
            return self._memory_workflows.get(workflow_id)

workflow_registry = WorkflowRegistry()
