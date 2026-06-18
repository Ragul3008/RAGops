from ragops_core.vectorstore.pg_store import PGVectorStore
from ragops_core.vectorstore.qdrant_store import QdrantVectorStore
from app.core.config import settings

def get_vectorstore(provider: str):
    if provider == "qdrant":
        return QdrantVectorStore(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
    else:
        return PGVectorStore(
            db_url=settings.DATABASE_URL
        )
