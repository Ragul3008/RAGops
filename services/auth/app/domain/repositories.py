from abc import ABC, abstractmethod
from uuid import UUID
from .entities import User

class IUserRepository(ABC):
    @abstractmethod
    async def find_by_id(
        self, user_id: UUID
    ) -> User | None: ...

    @abstractmethod
    async def find_by_email(
        self, email: str, tenant_id: UUID
    ) -> User | None: ...

    @abstractmethod
    async def save(self, user: User) -> User: ...

    @abstractmethod
    async def delete(
        self, user_id: UUID
    ) -> None: ...

class ITokenStore(ABC):
    @abstractmethod
    async def store_refresh(
        self, user_id: UUID, refresh_token: str
    ) -> None: ...