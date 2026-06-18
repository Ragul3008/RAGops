import numpy as np
from .dense import DenseRetriever

class MMRRetriever(DenseRetriever):
    """Maximal Marginal Relevance for
    diversity-aware retrieval."""
    
    async def retrieve(
        self, query_vector, tenant_id,
        top_k=5, lambda_mult=0.5, fetch_k=20,
    ):
        candidates = await super().retrieve(
            query_vector, tenant_id, top_k=fetch_k
        )
        return self._mmr_select(
            query_vector, candidates,
            top_k, lambda_mult
        )
    
    def _mmr_select(
        self, q, cands, k, lam
    ) -> list:
        selected, remaining = [], list(cands)
        while len(selected) < k and remaining:
            best = max(remaining, key=lambda c: (
                lam * c["score"] - (1 - lam) * max(
                    (np.dot(c["vector"], s["vector"])
                     for s in selected), default=0
                )
            ))
            selected.append(best)
            remaining.remove(best)
        return selected