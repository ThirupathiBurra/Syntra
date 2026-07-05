from abc import ABC, abstractmethod
from typing import List, Optional
from .models import AgentExecution, ExecutionQueue

class BaseScheduler(ABC):
    """
    Abstract Scheduler interface for determining execution order.
    """
    @abstractmethod
    def schedule(self, queue: ExecutionQueue) -> List[AgentExecution]:
        pass

class SequentialScheduler(BaseScheduler):
    """Schedules executions one after another."""
    def schedule(self, queue: ExecutionQueue) -> List[AgentExecution]:
        # Return next item in queue
        return queue.items[:1] if queue.items else []

class ParallelScheduler(BaseScheduler):
    """Schedules multiple independent executions simultaneously."""
    def schedule(self, queue: ExecutionQueue) -> List[AgentExecution]:
        # Return all independent items
        return queue.items

class DependencyAwareScheduler(BaseScheduler):
    """Schedules executions based on dependency resolution."""
    def schedule(self, queue: ExecutionQueue) -> List[AgentExecution]:
        # Complex scheduling logic goes here in the future
        return []
