try:
    from qdrant_client import AsyncQdrantClient
    from qdrant_client.models import (
        VectorParams, Distance,
        PointStruct, Filter, FieldCondition,
        MatchValue,
    )
    QDRANT_AVAILABLE = True
except ImportError as e:
    print(f"WARNING: Qdrant client could not be imported (cygrpc DLL blocked): {e}. Qdrant fallback will be used.")
    QDRANT_AVAILABLE = False
    AsyncQdrantClient = None
    VectorParams = Distance = PointStruct = Filter = FieldCondition = MatchValue = None

import numpy as np
import uuid
import json
import os
from .base import VectorStore

class QdrantVectorStore(VectorStore):
    """Qdrant implementation of VectorStore.
    Uses tenant_id as collection namespace for
    strict data isolation. Fallbacks to a local file store
    (local_vector_store.json) if Qdrant is offline."""
    
    def __init__(self, url: str, api_key: str):
        if QDRANT_AVAILABLE and AsyncQdrantClient is not None:
            try:
                client_kwargs = {"url": url, "check_compatibility": False}
                if api_key:
                    client_kwargs["api_key"] = api_key
                self.client = AsyncQdrantClient(**client_kwargs)
            except Exception as e:
                print(f"Failed to initialize AsyncQdrantClient: {e}")
                self.client = None
        else:
            self.client = None

    def _collection(
        self, tenant_id: str, name: str
    ) -> str:
        return f"{tenant_id}__{name}"

    def _read_local_store(self):
        file_path = "local_vector_store.json"
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _write_local_store(self, data):
        file_path = "local_vector_store.json"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to write to local fallback store: {e}")

    async def search(
        self, query_vector: np.ndarray,
        tenant_id: str, collection: str,
        top_k=10, score_threshold=0.7,
        filters=None,
    ) -> list[dict]:
        collection_name = self._collection(tenant_id, collection)
        try:
            if self.client is None or not QDRANT_AVAILABLE:
                raise RuntimeError("Qdrant client not available (cygrpc block)")
            results = await self.client.query_points(
                collection_name=collection_name,
                query=query_vector.tolist() if isinstance(query_vector, np.ndarray) else query_vector,
                limit=top_k,
                score_threshold=score_threshold,
                query_filter=self._build_filter(filters),
            )
            return [
                {"id": r.id,
                 "content": r.payload["content"],
                 "score":   r.score,
                 "metadata": r.payload.get("metadata")}
                for r in results.points
            ]
        except Exception as e:
            print(f"Qdrant search failed: {e}. Falling back to local file store.")
            
            # Read from JSON
            data = self._read_local_store()
            
            # Filter by collection
            filtered_points = [pt for pt in data if pt["collection"] == collection_name]
            if not filtered_points:
                return []
                
            q_vec = np.array(query_vector)
            q_norm = np.linalg.norm(q_vec)
            
            scored_results = []
            shape_mismatch_logged = False
            for pt in filtered_points:
                pt_vec = np.array(pt["vector"])
                if q_vec.shape != pt_vec.shape:
                    if not shape_mismatch_logged:
                        print(f"[ERROR] Vector shape mismatch: query shape is {q_vec.shape}, point shape is {pt_vec.shape}. Skipping comparison.")
                        shape_mismatch_logged = True
                    continue
                pt_norm = np.linalg.norm(pt_vec)
                if q_norm == 0 or pt_norm == 0:
                    similarity = 0.0
                else:
                    similarity = np.dot(q_vec, pt_vec) / (q_norm * pt_norm)
                
                # Check score threshold
                if similarity >= score_threshold:
                    scored_results.append({
                        "id": pt["id"],
                        "content": pt["payload"]["content"],
                        "score": float(similarity),
                        "metadata": pt["payload"].get("metadata")
                    })
            
            # Sort by score descending and return top_k
            scored_results.sort(key=lambda x: x["score"], reverse=True)
            return scored_results[:top_k]

    async def upsert(
        self, tenant_id: str, doc_id: str,
        chunks: list, vectors: list[np.ndarray],
    ) -> None:
        collection_name = self._collection(tenant_id, "documents")
        
        # Build the points list
        points_to_save = []
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
            points_to_save.append({
                "id": point_id,
                "vector": vec_list,
                "payload": payload,
                "collection": collection_name
            })
            
        # Try Qdrant first
        try:
            if self.client is None or not QDRANT_AVAILABLE:
                raise RuntimeError("Qdrant client not available (cygrpc block)")
            try:
                await self.client.get_collection(collection_name)
            except Exception:
                vector_size = len(vectors[0]) if vectors else 1536
                await self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE
                    )
                )
            
            q_points = [
                PointStruct(
                    id=pt["id"],
                    vector=pt["vector"],
                    payload=pt["payload"]
                )
                for pt in points_to_save
            ]
            if q_points:
                await self.client.upsert(
                    collection_name=collection_name,
                    points=q_points
                )
                print(f"[OK] Upserted {len(q_points)} points to Qdrant successfully.")
        except Exception as e:
            print(f"Qdrant upsert failed: {e}. Falling back to local file store.")
            # Save to JSON file
            data = self._read_local_store()
            # Remove any existing points for this doc_id in this collection to prevent duplicates
            data = [
                pt for pt in data 
                if not (pt["collection"] == collection_name and pt["payload"]["doc_id"] == str(doc_id))
            ]
            data.extend(points_to_save)
            self._write_local_store(data)
            print(f"[OK] Saved {len(points_to_save)} points to local fallback store (local_vector_store.json).")

    async def delete_document(
        self, tenant_id: str, doc_id: str
    ) -> None:
        collection_name = self._collection(tenant_id, "documents")
        try:
            if self.client is None or not QDRANT_AVAILABLE:
                raise RuntimeError("Qdrant client not available (cygrpc block)")
            await self.client.delete(
                collection_name=collection_name,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="doc_id",
                            match=MatchValue(value=str(doc_id))
                        )
                    ]
                )
            )
        except Exception as e:
            print(f"Qdrant delete failed: {e}. Falling back to local file store.")
            data = self._read_local_store()
            data = [
                pt for pt in data 
                if not (pt["collection"] == collection_name and pt["payload"]["doc_id"] == str(doc_id))
            ]
            self._write_local_store(data)

    async def get_collection_stats(
        self, tenant_id: str, collection: str
    ) -> dict:
        collection_name = self._collection(tenant_id, collection)
        try:
            if self.client is None or not QDRANT_AVAILABLE:
                raise RuntimeError("Qdrant client not available (cygrpc block)")
            info = await self.client.get_collection(collection_name)
            return {
                "points_count": info.points_count,
                "status": info.status
            }
        except Exception:
            data = self._read_local_store()
            filtered = [pt for pt in data if pt["collection"] == collection_name]
            if filtered:
                return {
                    "points_count": len(filtered),
                    "status": "green"
                }
            return {"points_count": 0, "status": "not_found"}

    def _build_filter(self, filters: dict | None) -> Filter | None:
        if not filters:
            return None
        conditions = []
        for key, val in filters.items():
            conditions.append(
                FieldCondition(
                    key=key,
                    match=MatchValue(value=val)
                )
            )
        return Filter(must=conditions)