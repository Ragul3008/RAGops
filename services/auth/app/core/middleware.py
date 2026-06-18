from starlette.middleware.base import (
    BaseHTTPMiddleware
)
from fastapi.responses import JSONResponse

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        tenant_id = request.headers.get(
            "X-Tenant-ID"
        )
        if not tenant_id:
            return JSONResponse(
                {"error": "Tenant required"},
                status_code=400
            )
        request.state.tenant_id = tenant_id
        return await call_next(request)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        return await call_next(request)