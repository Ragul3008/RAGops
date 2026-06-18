from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import UserModel
from app.domain.repositories import IUserRepository
from app.domain.entities import User
from uuid import UUID

class PgUserRepository(IUserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_id(
        self, user_id: UUID
    ) -> User | None:
        result = await self.db.get(
            UserModel, user_id
        )
        return result.to_domain() if result else None

    async def find_by_email(
        self, email: str, tenant_id: UUID
    ) -> User | None:
        stmt = select(UserModel).where(
            UserModel.email == email,
            UserModel.tenant_id == tenant_id,
        )
        result = await self.db.scalar(stmt)
        return result.to_domain() if result else None

    async def save(self, user: User) -> User:
        return user

    async def delete(self, user_id: UUID) -> None:
        pass