from functools import lru_cache
from app.infrastructure.azure.openai_provider import AzureOpenAIProvider
from app.infrastructure.azure.search_provider import AzureAISearchProvider
from app.application.rag.hybrid_retriever import HybridRetrieverService
from app.application.triage.crisis_triage import CrisisTriageService
from app.application.services.mental_health_orchestrator import MentalHealthOrchestrator

@lru_cache()
def get_openai_provider() -> AzureOpenAIProvider:
    return AzureOpenAIProvider()

@lru_cache()
def get_search_provider() -> AzureAISearchProvider:
    return AzureAISearchProvider()

@lru_cache()
def get_retriever_service() -> HybridRetrieverService:
    return HybridRetrieverService(vector_store=get_search_provider())

@lru_cache()
def get_triage_service() -> CrisisTriageService:
    return CrisisTriageService()

def get_mental_health_orchestrator() -> MentalHealthOrchestrator:
    return MentalHealthOrchestrator(
        llm_provider=get_openai_provider(),
        retriever=get_retriever_service(),
        triage_service=get_triage_service()
    )
