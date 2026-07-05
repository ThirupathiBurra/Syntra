from fastapi import APIRouter
from app.api.v1.endpoints import workflows, knowledge, planning, events, approvals

api_router = APIRouter()

api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
api_router.include_router(planning.router, prefix="/planning", tags=["planning"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(approvals.router, prefix="/approvals", tags=["approvals"])
