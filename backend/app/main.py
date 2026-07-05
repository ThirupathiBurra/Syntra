from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
import logging
from app.core.config import settings

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize components
from app.ai.agent_registry import agent_registry
from app.agents.knowledge.agent import knowledge_agent

# Register core agents
agent_registry.register(knowledge_agent)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Intelligence backend for Syntra Enterprise AI Platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["system"])
async def health_check():
    """Expanded health check endpoint for platform monitoring."""
    from app.ai.agent_registry import agent_registry
    from app.ai.providers import provider_registry
    from app.ai.orchestration.conductor import syntra_conductor
    
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "ai_core": {
            "status": "online",
            "registered_providers": provider_registry.list_providers(),
            "registered_agents": len(agent_registry.list_metadata()),
        },
        "conductor": {
            "status": "online" if syntra_conductor.is_healthy else "offline",
        }
    }

# Register API routers
from app.api.v1.router import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)
