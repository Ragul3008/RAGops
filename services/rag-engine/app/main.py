from fastapi import FastAPI
from app.api import router
from app.core.telemetry import setup_otel

app = FastAPI(title="RAGOps RAG Engine")
setup_otel(app, service_name="rag-engine")
app.include_router(router, prefix="/api/v1")