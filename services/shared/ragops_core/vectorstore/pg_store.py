import uuid
import numpy as np
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import Table, Column, String, Float, MetaData, Integer, select, delete, text
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from .base import VectorStore
import os

metadata = MetaData()
document_chunks = Table(
    "document_chunks", metadata,
    Column("id", String, primary_key=True),
    Column("tenant_id", String, index=True),
    Column("doc_id", String, index=True),
    Column("collection", String, index=True),
    Column("content", String),
    Column("metadata", JSONB),
    Column("embedding", Vector)
)

class PGVectorStore(VectorStore):
    """PostgreSQL implementation of VectorStore using pgvector.
    Uses tenant_id as collection namespace for strict data isolation."""
    
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url, future=True)
        self.initialized = False

    async def _init_db(self):
        if not self.initialized:
            async with self.engine.begin() as conn:
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                await conn.run_sync(metadata.create_all)
            self.initialized = True

    def _collection(self, tenant_id: str, name: str) -> str:
        return f"{tenant_id}__{name}"

    async def upsert(
        self, tenant_id: str, doc_id: str,
        chunks: list, vectors: list[np.ndarray],
    ) -> None:
        await self._init_db()
        collection_name = self._collection(tenant_id, "documents")
        
        insert_values = []
        for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{doc_id}_{i}"))
            vec_list = vector.tolist() if isinstance(vector, np.ndarray) else vector
            content = chunk.content if hasattr(chunk, "content") else chunk["content"]
            payload = {
                "content": content,
                "doc_id": str(doc_id),
                "index": chunk.index if hasattr(chunk, "index") else chunk.get("index", i),
                "metadata": {"doc_id": str(doc_id)}
            }
            
            insert_values.append({
                "id": point_id,
                "tenant_id": tenant_id,
                "doc_id": doc_id,
                "collection": collection_name,
                "content": content,
                "metadata": payload,
                "embedding": vec_list
            })
            
        if not insert_values:
            return
            
        async with self.engine.begin() as conn:
            # Upsert logic - since this is bulk insert, delete old chunks for this doc_id first
            # to keep it simple, or just insert (assuming unique IDs will conflict if not handled)
            # Actually, the base requirement is upsert, so let's delete existing first
            await conn.execute(delete(document_chunks).where(
                document_chunks.c.tenant_id == tenant_id,
                document_chunks.c.doc_id == doc_id
            ))
            await conn.execute(document_chunks.insert().values(insert_values))

    async def search(
        self, query_vector: np.ndarray,
        tenant_id: str, collection: str = "documents",
        top_k: int = 10,
        score_threshold: float = 0.7,
        filters: dict | None = None,
    ) -> list[dict]:
        await self._init_db()
        collection_name = self._collection(tenant_id, collection)
        
        vec_list = query_vector.tolist() if isinstance(query_vector, np.ndarray) else query_vector
        
        # pgvector supports cosine distance (<=>). Cosine similarity = 1 - distance
        distance = document_chunks.c.embedding.cosine_distance(vec_list).label("distance")
        
        stmt = select(document_chunks, distance).where(
            document_chunks.c.tenant_id == tenant_id,
            document_chunks.c.collection == collection_name
        )
        
        if filters:
            if "doc_id" in filters:
                stmt = stmt.where(document_chunks.c.doc_id == filters["doc_id"])
                
        stmt = stmt.order_by(distance).limit(top_k)
        
        async with self.engine.connect() as conn:
            result = await conn.execute(stmt)
            rows = result.fetchall()
            
            scored_results = []
            for row in rows:
                similarity = 1.0 - row.distance
                if similarity >= score_threshold:
                    scored_results.append({
                        "id": row.id,
                        "content": row.content,
                        "score": float(similarity),
                        "metadata": row.metadata
                    })
                    
            return scored_results

    async def delete_document(
        self, tenant_id: str, doc_id: str
    ) -> None:
        await self._init_db()
        async with self.engine.begin() as conn:
            stmt = delete(document_chunks).where(
                document_chunks.c.tenant_id == tenant_id,
                document_chunks.c.doc_id == doc_id
            )
            await conn.execute(stmt)

    async def get_collection_stats(
        self, tenant_id: str, collection: str = "documents"
    ) -> dict:
        await self._init_db()
        collection_name = self._collection(tenant_id, collection)
        
        async with self.engine.connect() as conn:
            stmt = select(document_chunks.c.id).where(
                document_chunks.c.tenant_id == tenant_id,
                document_chunks.c.collection == collection_name
            )
            result = await conn.execute(stmt)
            rows = result.fetchall()
            return {
                "vector_count": len(rows),
                "status": "green"
            }
