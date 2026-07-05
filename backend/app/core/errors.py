class SyntraError(Exception):
    """Base exception for all Syntra platform errors."""
    pass

class ConfigurationError(SyntraError):
    """Raised when the platform or an agent is misconfigured."""
    pass

class ValidationError(SyntraError):
    """Raised when inputs or outputs fail schema validation."""
    pass

class AIError(SyntraError):
    """Raised for general AI provider or inference errors."""
    pass

class WorkflowError(SyntraError):
    """Raised during execution of a workflow or task graph."""
    pass

class ToolError(SyntraError):
    """Raised when an external or internal tool fails to execute."""
    pass
