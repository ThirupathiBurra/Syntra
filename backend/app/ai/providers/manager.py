from typing import Dict, List, Optional
from .base import BaseProvider
from app.core.errors import ConfigurationError

class ProviderManager:
    """
    Manages registration, discovery, and selection of AI Providers.
    """
    
    def __init__(self):
        self._providers: Dict[str, BaseProvider] = {}
        self._default_provider: Optional[str] = None

    def register(self, provider: BaseProvider, set_as_default: bool = False) -> None:
        self._providers[provider.provider_name] = provider
        if set_as_default or self._default_provider is None:
            self._default_provider = provider.provider_name

    def get(self, provider_name: Optional[str] = None) -> BaseProvider:
        target = provider_name or self._default_provider
        if not target:
            raise ConfigurationError("No providers registered in ProviderManager")
        if target not in self._providers:
            # Fallback handling placeholder logic
            raise ConfigurationError(f"Provider '{target}' is not registered.")
        return self._providers[target]

    def list_providers(self) -> List[str]:
        return list(self._providers.keys())

    async def health_check_all(self) -> Dict[str, bool]:
        """Returns health status for all registered providers."""
        health = {}
        for name, provider in self._providers.items():
            try:
                health[name] = await provider.health_check()
            except Exception:
                health[name] = False
        return health

# Global singleton
provider_registry = ProviderManager()
provider_manager = provider_registry
