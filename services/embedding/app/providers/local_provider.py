import numpy as np
from .base import EmbeddingProvider

class LocalEmbeddingProvider(EmbeddingProvider):
    """Runs embedding locally via SentenceTransformers.
    Useful for air-gapped / on-prem deployments."""
    
    def __init__(self, model_name: str):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(
                "sentence-transformers is not installed. "
                "Please run `pip install sentence-transformers` to use local embeddings."
            )
        self.model = SentenceTransformer(
            model_name, device="cpu"
        )
    
    async def embed_texts(
        self, texts: list[str], **kwargs
    ) -> list[np.ndarray]:
        import asyncio
        loop = asyncio.get_event_loop()
        func = lambda: self.model.encode(texts, normalize_embeddings=True)
        embeddings = await loop.run_in_executor(None, func)
        return [np.array(e) for e in embeddings]

    async def embed_query(
        self, text: str
    ) -> np.ndarray:
        import asyncio
        loop = asyncio.get_event_loop()
        func = lambda: self.model.encode(text, normalize_embeddings=True)
        res = await loop.run_in_executor(None, func)
        return np.array(res)

    @property
    def dimensions(self) -> int:
        return self.model.get_sentence_embedding_dimension()

    @property
    def max_tokens(self) -> int:
        return getattr(self.model, "max_seq_length", 512)