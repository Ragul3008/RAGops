from abc import ABC, abstractmethod
import numpy as np

class EmbeddingProvider(ABC):
    """Abstract base for all embedding providers."""
    
    @abstractmethod
    async def embed_texts(
        self,
        texts: list[str],
        model: str | None = None,
    ) -> list[np.ndarray]:
        """Embed a batch of texts."""
        ...

    @abstractmethod
    async def embed_query(
        self, text: str
    ) -> np.ndarray:
        """Embed a single query text."""
        ...

    @property
    @abstractmethod
    def dimensions(self) -> int: ...

    @property
    @abstractmethod
    def max_tokens(self) -> int: ...