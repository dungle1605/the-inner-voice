import logging
from typing import List
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential
from app.core.config import settings
from app.domain.models import ChatMessage
from app.domain.protocols import LLMProviderProtocol
from app.core.exceptions import LLMProviderError

logger = logging.getLogger(__name__)

class AzureOpenAIProvider(LLMProviderProtocol):
    def __init__(self):
        self._deployment = settings.AZURE_OPENAI_MODEL_DEPLOYMENT_NAME
        try:
            if settings.AZURE_OPENAI_API_KEY and not settings.AZURE_OPENAI_API_KEY.startswith("<"):
                self._client = AzureOpenAI(
                    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                    api_key=settings.AZURE_OPENAI_API_KEY,
                    api_version=settings.OPENAI_API_VERSION
                )
            else:
                logger.info("Initializing Azure OpenAI using DefaultAzureCredential")
                token_credential = DefaultAzureCredential()
                self._client = AzureOpenAI(
                    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                    azure_ad_token_provider=lambda: token_credential.get_token("https://cognitiveservices.azure.com/.default").token,
                    api_version=settings.OPENAI_API_VERSION
                )
        except Exception as e:
            logger.error(f"Failed to initialize AzureOpenAI client: {e}")
            raise LLMProviderError(f"Azure OpenAI initialization failed: {e}")

    async def complete(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 600
    ) -> str:
        try:
            formatted = [{"role": m.role, "content": m.content} for m in messages]
            response = self._client.chat.completions.create(
                model=self._deployment,
                messages=formatted,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"AzureOpenAI chat completion error: {e}")
            raise LLMProviderError(f"Chat completion failed: {e}")
