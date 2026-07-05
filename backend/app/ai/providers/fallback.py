from typing import Any, AsyncGenerator
from .base import BaseProvider
from .models import Prompt, AIResponse, ModelConfig, GenerationConfig, SafetyConfig, RetryConfig, TimeoutConfig, UsageMetrics

class OpenRouterProvider(BaseProvider):
    """
    Fallback provider using OpenRouter.
    """
    
    provider_name = "openrouter"

    async def generate(self, prompt: Prompt, model_config: ModelConfig, gen_config: GenerationConfig, safety_config: SafetyConfig, retry_config: RetryConfig, timeout_config: TimeoutConfig) -> AIResponse:
        return AIResponse(
            content="[OpenRouter Fallback]",
            latency_ms=0, provider=self.provider_name, model=model_config.model_name, finish_reason="stop"
        )

    async def generate_structured(self, prompt: Prompt, schema: Any, model_config: ModelConfig, gen_config: GenerationConfig, safety_config: SafetyConfig, retry_config: RetryConfig, timeout_config: TimeoutConfig) -> AIResponse:
        return AIResponse(
            content="", structured_data={}, latency_ms=0, provider=self.provider_name, model=model_config.model_name, finish_reason="stop"
        )

    async def stream(self, prompt: Prompt, model_config: ModelConfig) -> AsyncGenerator[str, None]:
        yield "Fallback Chunk"

    async def health_check(self) -> bool:
        return True

    def count_tokens(self, prompt: Prompt, model_name: str) -> int:
        return 0

    def estimate_cost(self, prompt_tokens: int, completion_tokens: int, model_name: str) -> float:
        return 0.0

    def validate_request(self, prompt: Prompt, model_config: ModelConfig) -> bool:
        return True

    async def embed(self, texts: list[str], model_name: str) -> list[list[float]]:
        # Fallback currently mocks embedding
        return [[0.0] * 768 for _ in texts]
