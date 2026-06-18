from .dense import DenseRetriever
from .sparse import SparseRetriever
from app.reranking.cross_encoder import CrossEncoder

class HybridRetriever:
    """Combines dense + sparse retrieval with RRF
    (Reciprocal Rank Fusion) before reranking."""
    
    def __init__(self):
        self.dense  = DenseRetriever(...)
        self.sparse = SparseRetriever(...)
        self.reranker = CrossEncoder()

    async def retrieve(
        self, query: str, query_vector,
        tenant_id: str, top_k: int = 5,
    ) -> list[dict]:
        dense_r  = await self.dense.retrieve(
            query_vector, tenant_id, top_k=20
        )
        sparse_r = await self.sparse.retrieve(
            query, tenant_id, top_k=20
        )
        fused = self._rrf(dense_r, sparse_r)
        return await self.reranker.rerank(
            query, fused, top_k=top_k
        )

    def _rrf(self, *result_sets, k=60):
        scores: dict[str, float] = {}
        for rs in result_sets:
            for rank, doc in enumerate(rs):
                did = doc["id"]
                scores[did] = scores.get(did, 0) + 1.0 / (k + rank + 1)

        return sorted(
            scores.keys(),
            key=lambda d: scores[d],
            reverse=True,
        )