from .base import EmbeddingProvider
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import numpy as np
import asyncio

class GeminiEmbeddingProvider(EmbeddingProvider):
    """Google Gemini embedding provider using langchain-google-genai."""
    
    def __init__(self, api_key: str):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-2",
            google_api_key=api_key
        )
        
    async def embed_texts(
        self,
        texts: list[str],
        model: str | None = None,
    ) -> list[np.ndarray]:
        # Process in small batches and apply exponential backoff on 429 rate limit exceptions
        batch_size = 5
        results = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            for attempt in range(6):
                try:
                    res = await self.embeddings.aembed_documents(batch)
                    results.extend([np.array(r) for r in res])
                    break
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        sleep_time = (2 ** attempt) + 2
                        print(f"[WARN] Gemini embedding rate limited (429). Retrying batch {i//batch_size + 1} in {sleep_time}s... {e}")
                        await asyncio.sleep(sleep_time)
                    else:
                        raise e
            else:
                raise RuntimeError("Failed to embed batch after multiple attempts due to rate limits.")
            
            # Short delay between successful batches to prevent rate limiting
            await asyncio.sleep(0.5)
            
        return results

    async def embed_query(
        self, text: str
    ) -> np.ndarray:
        res = await self.embeddings.aembed_query(text)
        return np.array(res)

    @property
    def dimensions(self) -> int:
        return 3072

    @property
    def max_tokens(self) -> int:
        return 2048
