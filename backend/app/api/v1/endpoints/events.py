import asyncio
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.core.event_bus import event_bus

router = APIRouter()

async def event_generator(request: Request):
    """Generator for Server-Sent Events from the Event Bus."""
    queue = await event_bus.subscribe()
    try:
        while True:
            # Check if client disconnected
            if await request.is_disconnected():
                break
            
            # Wait for next event from bus
            # Use asyncio.wait_for to periodically check disconnect status
            try:
                payload = await asyncio.wait_for(queue.get(), timeout=1.0)
                yield f"data: {payload}\n\n"
            except asyncio.TimeoutError:
                # Keep-alive ping could be yielded here if needed
                continue
    finally:
        await event_bus.unsubscribe(queue)

@router.get("")
async def stream_events(request: Request):
    """
    Subscribe to live workflow execution events via Server-Sent Events.
    """
    return StreamingResponse(
        event_generator(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
