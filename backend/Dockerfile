FROM python:3.11-slim

WORKDIR /app

# Install uv for fast dependency resolution
RUN pip install uv

# Copy project specification files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv pip install --system .

# Copy application source
COPY app/ ./app/
COPY main.py ./

# Expose port (Cloud Run defaults to 8080, Railway uses PORT env var)
ENV PORT=8000
EXPOSE 8000

# Start Uvicorn
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
