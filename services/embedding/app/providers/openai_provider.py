import openai
import numpy as np
from .base import EmbeddingProvider

class OpenAIEmbeddingProvider(EmbeddingProvider):
    MODEL_DIMS = {
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "text-embedding-ada-002":  1536,
    }
    
    def __init__(self, api_key: str,
                 model="text-embedding-3-small"):
        self.client = openai.AsyncOpenAI(
            api_key=api_key
        )
        self.model = model

    async def embed_texts(
        self, texts: list[str], **kwargs
    ) -> list[np.ndarray]:
        resp = await self.client.embeddings.create(
            input=texts, model=self.model
        )
        return [
            np.array(d.embedding)
            for d in resp.data
        ]