from langchain_core.prompts import ChatPromptTemplate
from app.infrastructure.pg_prompt_store import (
    PgPromptStore
)

class PromptRegistry:
    """Versioned prompt store backed by PostgreSQL.
    Supports A/B testing and rollback."""
    
    _cache: dict[str, ChatPromptTemplate] = {}
    _store = PgPromptStore()
    
    @classmethod
    async def get(
        cls, version: str
    ) -> ChatPromptTemplate:
        if version not in cls._cache:
            record = await cls._store.get(version)
            cls._cache[version] = (
                ChatPromptTemplate.from_messages(
                    record.messages
                )
            )
        return cls._cache[version]

    @classmethod
    async def create_version(
        cls, messages: list, metadata: dict
    ) -> str:
        return await cls._store.create(
            messages=messages, metadata=metadata
        )