from typing import Protocol, List, Optional
from app.domain.models import ChatMessage, RetrievedSnippet

class LLMProviderProtocol(Protocol):
    """Protocol for LLM generation backends (Azure OpenAI, Local models, etc.)."""
    async def complete(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 600
    ) -> str:
        ...

class VectorStoreProtocol(Protocol):
    """Protocol for vector and hybrid search engines (Azure AI Search, Qdrant, etc.)."""
    async def search(
        self,
        query: str,
        top_k: int = 2
    ) -> List[RetrievedSnippet]:
        ...
