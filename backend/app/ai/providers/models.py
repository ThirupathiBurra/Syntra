from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class RetryConfig(BaseModel):
    max_retries: int = 3
    backoff_factor: float = 2.0
    initial_delay_ms: int = 1000

class TimeoutConfig(BaseModel):
    connect_timeout_ms: int = 5000
    read_timeout_ms: int = 30000

class SafetyConfig(BaseModel):
    harassment: str = "BLOCK_MEDIUM_AND_ABOVE"
    hate_speech: str = "BLOCK_MEDIUM_AND_ABOVE"
    sexually_explicit: str = "BLOCK_MEDIUM_AND_ABOVE"
    dangerous_content: str = "BLOCK_MEDIUM_AND_ABOVE"

class ModelConfig(BaseModel):
    model_name: str
    temperature: float = 0.0
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None

class GenerationConfig(BaseModel):
    stop_sequences: List[str] = Field(default_factory=list)
    response_format: Optional[Dict[str, Any]] = None
    json_mode: bool = False

class PromptMessage(BaseModel):
    role: str # "system", "user", "model", "developer"
    content: str

class Prompt(BaseModel):
    """Reusable prompt object for all agents."""
    messages: List[PromptMessage]
    context: str = ""
    variables: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class UsageMetrics(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

class AIResponse(BaseModel):
    """Standardized response model from any LLM provider."""
    content: str
    structured_data: Optional[Dict[str, Any]] = None
    citations: List[Any] = Field(default_factory=list)
    usage: UsageMetrics = Field(default_factory=UsageMetrics)
    latency_ms: int
    provider: str
    model: str
    finish_reason: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
