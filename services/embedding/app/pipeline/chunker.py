from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownTextSplitter,
)
from app.schemas.document import Chunk, ChunkStrategy

class DocumentChunker:
    SPLITTERS = {
        ChunkStrategy.RECURSIVE: (
            RecursiveCharacterTextSplitter
        ),
        ChunkStrategy.MARKDOWN: (
            MarkdownTextSplitter
        ),
    }

    def chunk(
        self,
        text: str,
        strategy: ChunkStrategy,
        chunk_size: int = 512,
        chunk_overlap: int = 64,
    ) -> list[Chunk]:
        cls = self.SPLITTERS[strategy]
        splitter = cls(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        texts = splitter.split_text(text)
        return [
            Chunk(content=t, index=i)
            for i, t in enumerate(texts)
        ]