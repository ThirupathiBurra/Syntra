# Syntra Enterprise AI Platform

"Where Intelligent Workflows Think, Decide, and Execute."

## Architecture

Syntra uses a decoupled architecture for maximum scalability and AI performance:
- **Frontend**: Next.js 15 (React), Tailwind CSS, shadcn/ui, Zustand, TanStack Query.
- **Backend (Intelligence Layer)**: FastAPI (Python 3.11+), LangGraph, LangChain, Pydantic, Alembic.

## Local Development Setup

### Prerequisites
- Node.js 20+
- Python 3.11+
- `uv` (Fast Python package manager)

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

## Environment Variables
Check the `.env.example` files in both `/frontend` and `/backend` directories for required configuration.

