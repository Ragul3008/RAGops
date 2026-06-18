from ragops_core.vectorstore.pg_store import PGVectorStore
from ragops_core.vectorstore.qdrant_store import QdrantVectorStore
from app.core.config import settings

class LocalDenseRetriever:
    def __init__(self, store):
        self.store = store

    async def retrieve(self, query_vector, tenant_id, top_k=5, collection="documents", score_threshold=0.7):
        return await self.store.search(
            query_vector=query_vector,
            tenant_id=tenant_id,
            collection=collection,
            top_k=top_k,
            score_threshold=score_threshold
        )

def get_retriever(metadata: dict):
    provider = metadata.get("vectorstore", "qdrant")
    if provider == "qdrant":
        store = QdrantVectorStore(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
    else:
        store = PGVectorStore(
            db_url=settings.DATABASE_URL
        )
    return LocalDenseRetriever(store)
