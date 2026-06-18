from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from uuid import UUID

from app.schemas.auth import (
    LoginRequest, TokenResponse,
    RefreshRequest
)
from app.services.auth_service import AuthService
from app.core.config import settings
from app.infrastructure.database import get_db
from app.infrastructure.pg_user_repo import PgUserRepository
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth")
security_scheme = HTTPBearer()

# Stub dummy token store since ITokenStore is abstract and has no concrete implementation in the repo
class DummyTokenStore:
    async def store_refresh(self, user_id: UUID, refresh_token: str) -> None:
        pass

async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    user_repo = PgUserRepository(db)
    token_store = DummyTokenStore()
    return AuthService(user_repo, token_store)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.JWT_PRIVATE_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/login")
async def login(
    req: LoginRequest,
    svc: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    return await svc.authenticate(req)

@router.post("/refresh")
async def refresh(
    req: RefreshRequest,
    svc: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    return await svc.refresh_token(req)

@router.post("/logout")
async def logout(
    token: str,
    svc: AuthService = Depends(get_auth_service)
) -> dict:
    return await svc.revoke_token(token)

@router.get("/me")
async def me(user: dict = Depends(get_current_user)) -> dict:
    return user