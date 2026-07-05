from typing import Dict, List, Optional
from pydantic import BaseModel
from .agent_base import BaseAgent, AgentMetadata

class RegistryHealth(BaseModel):
    status: str
    active_agents: int

class AgentRegistry:
    """Central registry for discovering and managing all AI agents in the platform."""
    
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        """Registers a new agent instance."""
        if agent.metadata.id in self._agents:
            raise ValueError(f"Agent with ID {agent.metadata.id} is already registered.")
        self._agents[agent.metadata.id] = agent

    def get(self, agent_id: str) -> BaseAgent:
        """Retrieves an agent by its ID."""
        if agent_id not in self._agents:
            raise KeyError(f"Agent {agent_id} not found in registry.")
        return self._agents[agent_id]

    def list_metadata(self) -> List[AgentMetadata]:
        """Returns metadata for all registered agents."""
        return [agent.metadata for agent in self._agents.values()]

    def health(self) -> RegistryHealth:
        """Returns the health status of the agent registry."""
        return RegistryHealth(
            status="healthy",
            active_agents=len(self._agents)
        )

# Global registry instance
agent_registry = AgentRegistry()
