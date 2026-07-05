from .manager import provider_registry
from .gemini import GeminiProvider
from .fallback import OpenRouterProvider

# Automatically register core providers
provider_registry.register(GeminiProvider(), set_as_default=True)
provider_registry.register(OpenRouterProvider())
