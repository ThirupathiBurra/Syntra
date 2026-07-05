import asyncio
from typing import AsyncGenerator
import json
import logging

logger = logging.getLogger(__name__)

class EventBus:
    """
    A lightweight, asyncio-based event bus for internal pub/sub.
    Used for broadcasting execution events to Server-Sent Events (SSE) endpoints.
    """
    def __init__(self):
        self._subscribers = []
        self._lock = asyncio.Lock()

    async def subscribe(self) -> asyncio.Queue:
        """Subscribe to the event bus and get an isolated queue."""
        queue = asyncio.Queue()
        async with self._lock:
            self._subscribers.append(queue)
        logger.debug(f"New subscriber added. Total subscribers: {len(self._subscribers)}")
        return queue

    async def unsubscribe(self, queue: asyncio.Queue):
        """Remove a subscription."""
        async with self._lock:
            if queue in self._subscribers:
                self._subscribers.remove(queue)
                logger.debug(f"Subscriber removed. Total subscribers: {len(self._subscribers)}")

    async def publish(self, event_type: str, data: dict):
        """Publish an event to all active subscribers."""
        event = {
            "type": event_type,
            "data": data
        }
        
        # Serialize to JSON string for SSE
        payload = json.dumps(event)
        
        async with self._lock:
            for queue in self._subscribers:
                try:
                    queue.put_nowait(payload)
                except Exception as e:
                    logger.error(f"Failed to publish event to subscriber: {e}")

# Global instance
event_bus = EventBus()
