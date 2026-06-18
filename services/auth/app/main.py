from fastapi import FastAPI
from app.api.v1 import router
from app.core.config import settings
from app.core.middleware import (
    TenantMiddleware,
    RateLimitMiddleware,
)

app = FastAPI(
    title="RAGOps Auth Service",
    version="1.0.0",
)

app.add_middleware(TenantMiddleware)
app.add_middleware(RateLimitMiddleware)
app.include_router(router, prefix="/api/v1")