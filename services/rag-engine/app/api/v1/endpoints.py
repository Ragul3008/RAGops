from fastapi import APIRouter, HTTPException
from app.graphs.rag_graph import build_rag_graph
from pydantic import BaseModel
from app.core.config import settings

router = APIRouter()

# Note: build_rag_graph will compile the state graph.
# Under some circumstances, importing nodes during compile time might fail if databases/services are not active.
# We will compile the graph when needed or wrap it.
try:
    graph = build_rag_graph()
except Exception:
    graph = None

class QueryRequest(BaseModel):
    query: str
    tenant_id: str
    llm_provider: str = "gemini"
    prompt_version: str = "v1"
    embedding_provider: str | None = None
    multi_query: bool = False
    rerank: bool = False
    top_k: int = 5
    score_threshold: float = 0.7

@router.get("/health")
async def health():
    return {"status": "healthy"}

@router.post("/query")
async def query_rag(req: QueryRequest):
    if graph is None:
        raise HTTPException(status_code=500, detail="RAG graph is not compiled successfully")
    inputs = {
        "query": req.query,
        "metadata": {
            "llm_provider": req.llm_provider,
            "prompt_version": req.prompt_version,
            "tenant_id": req.tenant_id,
            "embedding_provider": req.embedding_provider or settings.EMBEDDING_PROVIDER,
            "multi_query": req.multi_query,
            "rerank": req.rerank,
            "top_k": req.top_k,
            "score_threshold": req.score_threshold
        },
        "iteration": 0
    }
    result = await graph.ainvoke(inputs)
    return {
        "answer": result.get("answer"),
        "contexts": result.get("contexts", []),
        "route": result.get("route", ""),
        "rewritten_query": result.get("rewritten_query", ""),
        "faithful": result.get("faithful", True)
    }

