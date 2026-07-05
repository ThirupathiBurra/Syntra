from typing import List, Dict, Set
from .models import ExecutionGraph, CompiledNode, CompiledEdge
from app.ai.orchestration.models import ExecutionPlan
from app.core.errors import ValidationError

class GraphBuilder:
    """Builds an ExecutionGraph from an ExecutionPlan."""
    
    def build(self, plan: ExecutionPlan) -> ExecutionGraph:
        graph = ExecutionGraph()
        
        # 1. Create Nodes
        for step in plan.steps:
            node = CompiledNode(
                node_id=step.step_id,
                agent_id=step.target_agent_id or "system",
                dependencies=step.dependencies.depends_on
            )
            graph.nodes[node.node_id] = node
        
        # 2. Create Edges based on dependencies
        for node_id, node in graph.nodes.items():
            if not node.dependencies:
                graph.entry_nodes.append(node_id)
            for dep in node.dependencies:
                if dep in graph.nodes:
                    edge = CompiledEdge(source_id=dep, target_id=node_id)
                    graph.edges.append(edge)
                    
        # 3. Detect parallel groups / sequential chains (Placeholder)
        self._detect_groups(graph)
        
        return graph

    def _detect_groups(self, graph: ExecutionGraph) -> None:
        """Placeholder for parallel group detection."""
        pass
