import jwt
from app.core.config import settings
from app.domain.entities import User
from app.domain.repositories import IUserRepository, ITokenStore
from app.core.security import (
    create_access_token,
    verify_password,
    create_refresh_token,
)
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from ragops_core.exceptions import InvalidCredentials

class AuthService:
    def __init__(
        self,
        user_repo: IUserRepository,
        token_store: ITokenStore,
    ):
        self.user_repo = user_repo
        self.token_store = token_store

    async def authenticate(
        self, req: LoginRequest
    ):
        user = await self.user_repo.find_by_email(
            req.email, req.tenant_id
        )
        if not user or not verify_password(
            req.password, user.hashed_password
        ):
            raise InvalidCredentials()
        
        access = create_access_token(
            str(user.id),
            str(user.tenant_id),
            [r.value for r in user.roles],
        )
        refresh = create_refresh_token(str(user.id))
        await self.token_store.store_refresh(
            user.id, refresh
        )
        return TokenResponse(
            access_token=access,
            refresh_token=refresh,
        )

    async def refresh_token(self, req: RefreshRequest) -> TokenResponse:
        try:
            payload = jwt.decode(
                req.refresh_token,
                settings.JWT_PRIVATE_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            user_id = payload.get("sub")
            # Generate new access token
            access = create_access_token(user_id, "default-tenant", ["member"])
            return TokenResponse(
                access_token=access,
                refresh_token=req.refresh_token
            )
        except Exception:
            raise InvalidCredentials()

    async def revoke_token(self, token: str) -> dict:
        return {"message": "Logged out successfully"}