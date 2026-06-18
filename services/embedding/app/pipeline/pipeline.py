from .parser import DocumentParser
from .chunker import DocumentChunker
from .cleaner import TextCleaner
from app.providers.factory import get_embedding_provider
from app.vectorstore.factory import get_vectorstore

class EmbeddingPipeline:
    """Orchestrates the full document ingestion
    pipeline: parse → clean → chunk → embed → store."""
    
    def __init__(self):
        self.parser  = DocumentParser()
        self.cleaner = TextCleaner()
        self.chunker = DocumentChunker()
    
    async def ingest(
        self, doc_id: str, content: bytes,
        filename: str, tenant_id: str,
        config: PipelineConfig,
    ):
        raw     = await self.parser.parse(content, filename)
        cleaned = self.cleaner.clean(raw)
        chunks  = self.chunker.chunk(
            cleaned, config.strategy,
            config.chunk_size, config.chunk_overlap
        )
        provider = get_embedding_provider(
            config.embedding_provider
        )
        vectors = await provider.embed_texts(
            [c.content for c in chunks]
        )
        store = get_vectorstore(config.vectorstore)
        await store.upsert(
            tenant_id=tenant_id,
            doc_id=doc_id,
            chunks=chunks,
            vectors=vectors,
        )