from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

def get_llm(provider: str, **kwargs):
    match provider:
        case "openai":
            return ChatOpenAI(
                model=kwargs.get("model","gpt-4o"),
                temperature=kwargs.get("temperature",0),
                api_key=settings.OPENAI_API_KEY
            )
        case "anthropic":
            return ChatAnthropic(
                model=kwargs.get("model", "claude-3-5-sonnet-20241022"),
                api_key=settings.ANTHROPIC_API_KEY
            )
        case "gemini":
            return ChatGoogleGenerativeAI(
                model=kwargs.get("model","gemini-3.1-flash-lite"),
                google_api_key=settings.GOOGLE_API_KEY
            )
        case "ollama":
            base_url = settings.OLLAMA_BASE_URL or "http://localhost:11434"
            model_name = kwargs.get("model", settings.OLLAMA_MODEL or "qwen3:8b")
            return ChatOpenAI(
                base_url=f"{base_url.rstrip('/')}/v1",
                api_key="ollama",
                model=model_name,
                temperature=kwargs.get("temperature", 0)
            )
        case _:
            raise ValueError(
                f"Unknown LLM provider: {provider}"
            )