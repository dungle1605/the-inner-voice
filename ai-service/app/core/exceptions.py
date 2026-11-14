class AIException(Exception):
    """Base exception for all AI microservice domain errors."""
    pass

class SafetyPolicyViolationError(AIException):
    """Raised when user input or model output violates safety/ethics guidelines."""
    pass

class LLMProviderError(AIException):
    """Raised when an external LLM provider call fails."""
    pass

class VectorStoreError(AIException):
    """Raised when vector search fails."""
    pass
