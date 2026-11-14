import logging
from typing import List
from app.domain.models import RetrievedSnippet
from app.domain.protocols import VectorStoreProtocol

logger = logging.getLogger(__name__)

class HybridRetrieverService:
    def __init__(self, vector_store: VectorStoreProtocol):
        self._vector_store = vector_store

    async def retrieve_context(self, query: str, top_k: int = 2) -> List[RetrievedSnippet]:
        try:
            return await self._vector_store.search(query=query, top_k=top_k)
        except Exception as e:
            logger.warning(f"Hybrid retrieval bypassed due to error: {e}")
            return []
