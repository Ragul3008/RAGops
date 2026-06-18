from abc import ABC, abstractmethod
import numpy as np

class VectorStore(ABC):
    """Abstract base for all vector databases.
    Enables swapping Qdrant, Pinecone, Weaviate
    or pgvector without changing business logic."""
    
    @abstractmethod
    async def upsert(
        self, tenant_id: str, doc_id: str,
        chunks: list, vectors: list[np.ndarray],
    ) -> None: ...

    @abstractmethod
    async def search(
        self, query_vector: np.ndarray,
        tenant_id: str, collection: str,
        top_k: int = 10,
        score_threshold: float = 0.7,
        filters: dict | None = None,
    ) -> list[dict]: ...

    @abstractmethod
    async def delete_document(
        self, tenant_id: str, doc_id: str
    ) -> None: ...

    @abstractmethod
    async def get_collection_stats(
        self, tenant_id: str, collection: str
    ) -> dict: ...