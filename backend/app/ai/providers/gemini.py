import time
from typing import Any, AsyncGenerator, Optional
from .base import BaseProvider
from app.core.config import settings
from .models import (
    Prompt,
    AIResponse,
    ModelConfig,
    GenerationConfig,
    SafetyConfig,
    RetryConfig,
    TimeoutConfig,
    UsageMetrics
)
from app.core.logging import get_agent_logger
from app.core.errors import AIError

logger = get_agent_logger()

class GeminiProvider(BaseProvider):
    """
    Production implementation of the Google Gemini provider.
    Currently acts as structural architecture; no direct API calls exist yet.
    """
    
    provider_name = "gemini"

    async def generate(
        self, 
        prompt: Prompt | str, 
        model_config: Optional[ModelConfig] = None, 
        gen_config: Optional[GenerationConfig] = None, 
        safety_config: Optional[SafetyConfig] = None,
        retry_config: Optional[RetryConfig] = None,
        timeout_config: Optional[TimeoutConfig] = None
    ) -> AIResponse:
        model_name = model_config.model_name if model_config else "models/gemini-2.5-flash"
        logger.info("provider_generate_started", f"Starting generation via {self.provider_name}", {"model": model_name})
        start_time = time.time()
        
        prompt_text = prompt.messages[-1].content if isinstance(prompt, Prompt) else prompt

        content = "[Gemini API key missing or failed]"
        import os
        api_key = settings.GEMINI_API_KEY
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                # Note: google.generativeai expects 'models/gemini-pro' or 'gemini-2.5-flash' etc.
                model_name_clean = model_name.replace("models/", "")
                model = genai.GenerativeModel(model_name_clean)
                res = model.generate_content(prompt_text)
                content = res.text
            except Exception as e:
                logger.error("provider_generation_failed", str(e))
                content = f"Error generating content: {e}"
        else:
            logger.warning("provider_generation_warning", "No GEMINI_API_KEY. Using mock content.")
            content = "[Mock Content due to missing API Key]"
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        return AIResponse(
            content=content,
            latency_ms=latency_ms,
            provider=self.provider_name,
            model=model_name,
            finish_reason="stop",
            usage=UsageMetrics(prompt_tokens=0, completion_tokens=0, total_tokens=0)
        )

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
        logger.info("provider_structured_generate_started", f"Starting structured generation via {self.provider_name}", {"model": model_config.model_name})
        
        # Architecture placeholder for JSON Response Mode
        # Will pass `schema` to Gemini's `response_schema` param
        
        return AIResponse(
            content="",
            structured_data={"placeholder": "data matching schema"},
            latency_ms=100,
            provider=self.provider_name,
            model=model_config.model_name,
            finish_reason="stop"
        )

    async def stream(
        self, 
        prompt: Prompt, 
        model_config: ModelConfig
    ) -> AsyncGenerator[str, None]:
        # Architecture placeholder for streaming support
        yield "Chunk 1"
        yield "Chunk 2"

    async def health_check(self) -> bool:
        # Architecture placeholder: verify GOOGLE_API_KEY
        return True

    def count_tokens(self, prompt: Prompt, model_name: str) -> int:
        return 0

    def estimate_cost(self, prompt_tokens: int, completion_tokens: int, model_name: str) -> float:
        return 0.0

    def validate_request(self, prompt: Prompt, model_config: ModelConfig) -> bool:
        if not model_config.model_name.startswith("gemini"):
            return False
        return True

    async def embed(self, texts: list[str], model_name: str = "models/text-embedding-004") -> list[list[float]]:
        logger.info("provider_embedding_started", "Generating embeddings via REST", {"model": model_name, "count": len(texts)})
        try:
            import os
            import aiohttp
            api_key = settings.GEMINI_API_KEY
            if not api_key:
                logger.warning("provider_embedding_warning", "No GEMINI_API_KEY. Using mock embeddings.")
                return [[0.1] * 768 for _ in texts]
                
            embeddings = []
            async with aiohttp.ClientSession() as session:
                for text in texts:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent?key={api_key}"
                    payload = {
                        "model": "models/text-embedding-004",
                        "content": {
                            "parts": [{"text": text}]
                        },
                        "taskType": "RETRIEVAL_DOCUMENT"
                    }
                    async with session.post(url, json=payload, timeout=10) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            embeddings.append(data.get("embedding", {}).get("values", [0.0]*768))
                        else:
                            logger.error("provider_embedding_failed", await resp.text())
                            embeddings.append([0.0]*768)
            return embeddings
        except Exception as e:
            logger.error("provider_embedding_failed", str(e))
            raise AIError(f"Embedding failed: {str(e)}")
