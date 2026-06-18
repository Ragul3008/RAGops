from app.core.config import settings
import numpy as np

class LocalOpenAIEmbedder:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def embed_query(self, text: str) -> np.ndarray:
        import openai
        client = openai.AsyncOpenAI(api_key=self.api_key)
        resp = await client.embeddings.create(
            input=[text], model="text-embedding-3-small"
        )
        return np.array(resp.data[0].embedding)

class LocalGeminiEmbedder:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def embed_query(self, text: str) -> np.ndarray:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-2",
            google_api_key=self.api_key
        )
        res = await embeddings.aembed_query(text)
        return np.array(res)

_local_model_cache = {}

class LocalSentenceTransformerEmbedder:
    def __init__(self, model_name: str):
        self.model_name = model_name

    async def embed_query(self, text: str) -> np.ndarray:
        global _local_model_cache
        if self.model_name not in _local_model_cache:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError:
                raise ImportError(
                    "sentence-transformers is not installed. "
                    "Please run `pip install sentence-transformers` to use local embeddings."
                )
            _local_model_cache[self.model_name] = SentenceTransformer(
                self.model_name, device="cpu"
            )
        
        model = _local_model_cache[self.model_name]
        import asyncio
        loop = asyncio.get_event_loop()
        func = lambda: model.encode(text, normalize_embeddings=True)
        res = await loop.run_in_executor(None, func)
        return np.array(res)

def get_embedder(metadata: dict):
    provider = metadata.get("embedding_provider", settings.EMBEDDING_PROVIDER)
    if provider in ("gemini", "google"):
        return LocalGeminiEmbedder(api_key=settings.GOOGLE_API_KEY)
    elif provider == "local":
        return LocalSentenceTransformerEmbedder(model_name=settings.LOCAL_MODEL)
    else:
        return LocalOpenAIEmbedder(api_key=settings.OPENAI_API_KEY)
