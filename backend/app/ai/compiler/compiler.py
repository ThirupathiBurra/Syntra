from datetime import datetime, timezone
from app.ai.orchestration.models import ExecutionPlan
from app.core.errors import ValidationError
from app.core.logging import get_workflow_logger
from .models import CompiledWorkflow, ExecutionMetadata, ExecutionGraph
from .graph_builder import GraphBuilder

logger = get_workflow_logger()

class ExecutionCompiler:
    """
    Converts an AI-generated ExecutionPlan into an executable CompiledWorkflow.
    Framework-independent; contains NO execution or AI logic.
    """
    
    def __init__(self):
        self.graph_builder = GraphBuilder()

    def compile(self, plan: ExecutionPlan) -> CompiledWorkflow:
        logger.info("compiler_started", "Compiling ExecutionPlan", {"plan_id": plan.plan_id})
        
        # 1. Build Graph
        graph = self.graph_builder.build(plan)
        
        # 2. Validate Graph
        self._validate_graph(graph)
        
        # 3. Optimize Graph (Placeholder)
        self._optimize_graph(graph)
        
        # 4. Generate Metadata
        metadata = ExecutionMetadata(
            compiled_at=datetime.now(timezone.utc).isoformat(),
            total_nodes=len(graph.nodes),
            total_edges=len(graph.edges),
            is_parallelizable=len(graph.edges) < len(graph.nodes) - 1 # Basic placeholder
        )
        
        workflow = CompiledWorkflow(
            workflow_id=plan.workflow_id,
            plan_id=plan.plan_id,
            graph=graph,
            metadata=metadata
        )
        
        logger.info("compiler_completed", "ExecutionPlan compiled successfully", {"workflow_id": workflow.workflow_id})
        return workflow

    def _validate_graph(self, graph: ExecutionGraph) -> None:
        """Validates graph safety (unreachable nodes, circular dependencies)."""
        if not graph.nodes:
            logger.warning("compiler_validation_warning", "Graph has no nodes")
            return
            
        if not graph.entry_nodes:
            raise ValidationError("Graph has no entry nodes (possible circular dependency).")

        # Basic unreachable nodes check
        reachable = set(graph.entry_nodes)
        added = True
        while added:
            added = False
            for edge in graph.edges:
                if edge.source_id in reachable and edge.target_id not in reachable:
                    reachable.add(edge.target_id)
                    added = True
                    
        unreachable = set(graph.nodes.keys()) - reachable
        if unreachable:
            raise ValidationError(f"Graph contains unreachable nodes: {unreachable}")

    def _optimize_graph(self, graph: ExecutionGraph) -> None:
        """Placeholder for batching, simplification, and parallel optimization."""
        pass

# Singleton
execution_compiler = ExecutionCompiler()
