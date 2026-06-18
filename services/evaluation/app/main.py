from fastapi import FastAPI
from app.api import router
from app.core.telemetry import setup_otel

app = FastAPI(title="RAGOps Evaluation Service")
setup_otel(app, service_name="evaluation-service")
app.include_router(router, prefix="/api/v1")