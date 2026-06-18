import numpy as np
from app.vectorstore.base import VectorStore

class DenseRetriever:
    """Standard ANN vector similarity search."""
    
    def __init__(self, store: VectorStore):
        self.store = store

    async def retrieve(
        self,
        query_vector: np.ndarray,
        tenant_id: str,
        collection: str,
        top_k: int = 10,
        score_threshold: float = 0.7,
    ) -> list[dict]:
        return await self.store.search(
            query_vector=query_vector,
            tenant_id=tenant_id,
            collection=collection,
            top_k=top_k,
            score_threshold=score_threshold,
        )