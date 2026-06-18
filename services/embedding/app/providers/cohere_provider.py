import cohere
import numpy as np
from .base import EmbeddingProvider

class CohereEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str):
        self.client = cohere.AsyncClient(api_key)
        self._model = "embed-english-v3.0"

    async def embed_texts(
        self, texts: list[str], **kwargs
    ) -> list[np.ndarray]:
        resp = await self.client.embed(
            texts=texts,
            model=self._model,
            input_type="search_document",
        )
        return [np.array(v) for v in resp.embeddings]