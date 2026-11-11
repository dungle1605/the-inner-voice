import logging
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from app.config import settings

logger = logging.getLogger(__name__)

def get_openai_client() -> AzureOpenAI:
    """
    Khởi tạo Azure OpenAI Client.
    Ưu tiên sử dụng API Key nếu có trong .env, nếu không sử dụng Managed Identity (DefaultAzureCredential).
    """
    if settings.AZURE_OPENAI_API_KEY and not settings.AZURE_OPENAI_API_KEY.startswith("<"):
        return AzureOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.OPENAI_API_VERSION
        )
    else:
        logger.info("Using DefaultAzureCredential for Azure OpenAI")
        token_credential = DefaultAzureCredential()
        return AzureOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            azure_ad_token_provider=lambda: token_credential.get_token("https://cognitiveservices.azure.com/.default").token,
            api_version=settings.OPENAI_API_VERSION
        )

def get_search_client():
    """
    Khởi tạo Azure AI Search Client nếu đã được cấu hình endpoint và key hợp lệ.
    """
    if (settings.AZURE_SEARCH_ENDPOINT 
        and not settings.AZURE_SEARCH_ENDPOINT.startswith("<")
        and settings.AZURE_SEARCH_KEY 
        and not settings.AZURE_SEARCH_KEY.startswith("<")):
        try:
            return SearchClient(
                endpoint=settings.AZURE_SEARCH_ENDPOINT,
                index_name=settings.AZURE_SEARCH_INDEX_NAME,
                credential=AzureKeyCredential(settings.AZURE_SEARCH_KEY)
            )
        except Exception as e:
            logger.warning(f"Could not initialize Azure AI Search client: {e}")
            return None
    return None

