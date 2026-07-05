from typing import List, Tuple
from .models import GeneratedWorkflow
from .registry import workflow_registry

class WorkflowValidator:
    """
    Validates a generated workflow against registered capabilities.
    """
    
    def validate(self, workflow: GeneratedWorkflow) -> Tuple[bool, List[str]]:
        errors = []
        available_caps = {cap.id for cap in workflow_registry.get_capabilities()}
        
        for node in workflow.nodes:
            if node.capability_id not in available_caps:
                errors.append(f"Node '{node.node_id}' uses unsupported capability '{node.capability_id}'. Available: {', '.join(available_caps)}")
                
        # Validate dependencies exist
        node_ids = {node.node_id for node in workflow.nodes}
        for node_id, deps in workflow.dependencies.items():
            if node_id not in node_ids:
                errors.append(f"Dependency mapped for non-existent node '{node_id}'")
            for dep in deps:
                if dep not in node_ids:
                    errors.append(f"Node '{node_id}' depends on non-existent node '{dep}'")
                    
        return len(errors) == 0, errors

workflow_validator = WorkflowValidator()
