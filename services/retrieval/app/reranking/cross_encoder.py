from sentence_transformers import CrossEncoder as CE

class CrossEncoder:
    """Cross-encoder reranker for high-precision
    relevance scoring after initial retrieval."""
    
    def __init__(
        self,
        model="cross-encoder/ms-marco-MiniLM-L-12-v2"
    ):
        self.model = CE(model)

    async def rerank(
        self,
        query: str,
        docs: list[dict],
        top_k: int = 5,
    ) -> list[dict]:
        pairs = [(query, d["content"]) for d in docs]
        scores = self.model.predict(pairs)
        ranked = sorted(
            zip(docs, scores),
            key=lambda x: x[1],
            reverse=True,
        )
        return [d for d, _ in ranked[:top_k]]