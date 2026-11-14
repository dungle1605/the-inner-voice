import logging
from typing import List
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from app.config import settings
from app.domain.models import RetrievedSnippet
from app.domain.protocols import VectorStoreProtocol
from app.core.exceptions import VectorStoreError

logger = logging.getLogger(__name__)

class AzureAISearchProvider(VectorStoreProtocol):
    def __init__(self):
        self._client = None
        if (settings.AZURE_SEARCH_ENDPOINT 
            and not settings.AZURE_SEARCH_ENDPOINT.startswith("<")
            and settings.AZURE_SEARCH_KEY 
            and not settings.AZURE_SEARCH_KEY.startswith("<")):
            try:
                self._client = SearchClient(
                    endpoint=settings.AZURE_SEARCH_ENDPOINT,
                    index_name=settings.AZURE_SEARCH_INDEX_NAME,
                    credential=AzureKeyCredential(settings.AZURE_SEARCH_KEY)
                )
            except Exception as e:
                logger.warning(f"Could not connect to Azure AI Search: {e}")
                self._client = None

    async def search(self, query: str, top_k: int = 2) -> List[RetrievedSnippet]:
        if not self._client:
            return []

        try:
            results = self._client.search(search_text=query, top=top_k)
            snippets: List[RetrievedSnippet] = []
            for doc in results:
                content = doc.get("content", "")
                title = doc.get("title", "Tài liệu tâm lý")
                source = doc.get("source", "WHO / UNICEF Mental Health Guidelines")
                score = doc.get("@search.score", 0.0)
                if content:
                    snippets.append(RetrievedSnippet(title=title, content=content, source=source, relevance_score=score))
            return snippets
        except Exception as e:
            logger.error(f"Error querying Azure AI Search: {e}")
            raise VectorStoreError(f"Vector search failed: {e}")
