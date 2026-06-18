from enum import Enum
from pydantic import BaseModel

class ChunkStrategy(str, Enum):
    RECURSIVE = "recursive"
    MARKDOWN = "markdown"

class Chunk(BaseModel):
    content: str
    index: int

class PipelineConfig(BaseModel):
    strategy: ChunkStrategy = ChunkStrategy.RECURSIVE
    chunk_size: int = 512
    chunk_overlap: int = 64
    embedding_provider: str = "openai"
    vectorstore: str = "qdrant"
