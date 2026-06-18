from app.core.config import settings
from .base import EmbeddingProvider
from .openai_provider import OpenAIEmbeddingProvider
from .cohere_provider import CohereEmbeddingProvider
from .local_provider import LocalEmbeddingProvider
from .gemini_provider import GeminiEmbeddingProvider

def get_embedding_provider(
    provider: str = "openai",
) -> EmbeddingProvider:
    match provider:
        case "openai":
            return OpenAIEmbeddingProvider(
                api_key=settings.OPENAI_API_KEY
            )
        case "cohere":
            return CohereEmbeddingProvider(
                api_key=settings.COHERE_API_KEY
            )
        case "local":
            return LocalEmbeddingProvider(
                model_name=settings.LOCAL_MODEL
            )
        case "gemini" | "google":
            return GeminiEmbeddingProvider(
                api_key=settings.GOOGLE_API_KEY
            )
        case _:
            raise ValueError(
                f"Unknown provider: {provider}"
            )