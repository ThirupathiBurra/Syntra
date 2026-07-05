import os
import time
import logging
from typing import AsyncGenerator, Any
from groq import AsyncGroq
from app.core.config import settings

from .base import BaseProvider
from .models import Prompt, AIResponse, ModelConfig, GenerationConfig, SafetyConfig, RetryConfig, TimeoutConfig

logger = logging.getLogger(__name__)

class GroqProvider(BaseProvider):
    """
    AI Provider for Groq's high-speed inference engine.
    """
    provider_name = "groq"

    def __init__(self):
        super().__init__()
        # Initialize with a dummy key if missing to prevent Uvicorn from crashing on boot.
        # It will fail gracefully during execution and fallback to Gemini.
        api_key = settings.GROQ_API_KEY or "missing_key"
        self.client = AsyncGroq(api_key=api_key)

    async def generate(self, prompt: Prompt, model_config: ModelConfig, gen_config: GenerationConfig, safety_config: SafetyConfig, retry_config: RetryConfig, timeout_config: TimeoutConfig) -> AIResponse:
        start_time = time.time()
        
        # Use llama-3.3-70b-versatile as default Groq model if not specified
        model = model_config.model_name if "llama" in model_config.model_name.lower() or "mixtral" in model_config.model_name.lower() else "llama-3.3-70b-versatile"
        
        messages = []
        if prompt.system:
            messages.append({"role": "system", "content": prompt.system})
        
        # Combine user prompt and context
        full_user_content = prompt.user
        if prompt.context:
            full_user_content += f"\n\nContext:\n{prompt.context}"
            
        messages.append({"role": "user", "content": full_user_content})

        # Execute Groq completion
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=gen_config.temperature,
            max_tokens=gen_config.max_output_tokens,
            top_p=gen_config.top_p,
        )
        
        content = response.choices[0].message.content
        latency_ms = int((time.time() - start_time) * 1000)

        return AIResponse(
            content=content,
            latency_ms=latency_ms,
            provider=self.provider_name,
            model=model,
            finish_reason=response.choices[0].finish_reason
        )

    async def generate_structured(self, prompt: Prompt, schema: Any, model_config: ModelConfig, gen_config: GenerationConfig, safety_config: SafetyConfig, retry_config: RetryConfig, timeout_config: TimeoutConfig) -> AIResponse:
        # Since the DAG compiler passes Pydantic models in `schema`, and Groq's JSON mode doesn't take 
        # a strict Pydantic model natively like Gemini does, we will instruct the model to return JSON
        # and enforce json_object response_format.
        
        start_time = time.time()
        model = model_config.model_name if "llama" in model_config.model_name.lower() or "mixtral" in model_config.model_name.lower() else "llama-3.3-70b-versatile"
        
        system_instruction = prompt.system or "You are a helpful API that outputs only valid JSON."
        system_instruction += f"\n\nYou MUST return your response as a valid JSON object matching this schema:\n{schema.model_json_schema()}"
        
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt.user}
        ]
        
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=gen_config.temperature,
            max_tokens=gen_config.max_output_tokens,
            top_p=gen_config.top_p,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        latency_ms = int((time.time() - start_time) * 1000)
        
        import json
        structured_data = {}
        try:
            structured_data = json.loads(content)
        except Exception as e:
            logger.error(f"Failed to parse Groq JSON response: {e}")
            
        return AIResponse(
            content=content,
            structured_data=structured_data,
            latency_ms=latency_ms,
            provider=self.provider_name,
            model=model,
            finish_reason=response.choices[0].finish_reason
        )

    async def stream(self, prompt: Prompt, model_config: ModelConfig) -> AsyncGenerator[str, None]:
        # Implementation placeholder
        yield "Streaming not implemented for Groq yet"

    async def health_check(self) -> bool:
        if not settings.GROQ_API_KEY:
            return False
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False

    def count_tokens(self, prompt: Prompt, model_name: str) -> int:
        return 0

    def estimate_cost(self, prompt_tokens: int, completion_tokens: int, model_name: str) -> float:
        return 0.0

    def validate_request(self, prompt: Prompt, model_config: ModelConfig) -> bool:
        return True

    async def embed(self, texts: list[str], model_name: str) -> list[list[float]]:
        # Groq does not currently provide text embedding models
        raise NotImplementedError("Groq does not support embeddings")
