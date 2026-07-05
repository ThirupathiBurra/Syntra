from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Optional
from .models import (
    Prompt,
    AIResponse,
    ModelConfig,
    GenerationConfig,
    SafetyConfig,
    RetryConfig,
    TimeoutConfig
)

class BaseProvider(ABC):
    """
    Abstract interface for all AI Providers (Gemini, OpenRouter, etc.).
    """
    
    provider_name: str

    @abstractmethod
    async def generate(
        self, 
        prompt: Prompt | str, 
        model_config: Optional[ModelConfig] = None, 
        gen_config: Optional[GenerationConfig] = None, 
        safety_config: Optional[SafetyConfig] = None,
        retry_config: Optional[RetryConfig] = None,
        timeout_config: Optional[TimeoutConfig] = None
    ) -> AIResponse:
        """Standard text generation."""
        pass

    @abstractmethod
    async def generate_structured(
        self, 
        prompt: Prompt | str, 
        schema: Any,
        model_config: Optional[ModelConfig] = None,
        gen_config: Optional[GenerationConfig] = None,
        safety_config: Optional[SafetyConfig] = None,
        retry_config: Optional[RetryConfig] = None,
        timeout_config: Optional[TimeoutConfig] = None
    ) -> AIResponse:
        """Generation enforcing a strict JSON schema output."""
        pass

    @abstractmethod
    async def stream(
        self, 
        prompt: Prompt, 
        model_config: ModelConfig
    ) -> AsyncGenerator[str, None]:
        """Streaming response generator."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Verifies connection and authentication to the provider."""
        pass

    @abstractmethod
    def count_tokens(self, prompt: Prompt, model_name: str) -> int:
        """Estimates the token count for a given prompt without executing."""
        pass

    @abstractmethod
    def estimate_cost(self, prompt_tokens: int, completion_tokens: int, model_name: str) -> float:
        """Estimates the USD cost of an operation."""
        pass

    @abstractmethod
    def validate_request(self, prompt: Prompt, model_config: ModelConfig) -> bool:
        """Validates if the prompt and config are valid for this provider."""
        pass

    @abstractmethod
    async def embed(self, texts: list[str], model_name: str) -> list[list[float]]:
        """Generates embeddings for a list of strings."""
        pass
