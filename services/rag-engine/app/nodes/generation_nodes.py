from app.llm.factory import get_llm
from app.prompts.registry import PromptRegistry
from app.state import RAGState
from langchain_core.prompts import ChatPromptTemplate


def _extract_text(content) -> str:
    """Normalize LLM response content to a plain string.

    Different providers return different types from message.content:
    - OpenAI / Gemini: str
    - Anthropic Claude: list of content blocks, e.g.
        [{'type': 'text', 'text': '...', 'extras': {...}}]
    """
    import ast

    if isinstance(content, str):
        content_stripped = content.strip()
        if content_stripped.startswith("[") and content_stripped.endswith("]"):
            try:
                parsed = ast.literal_eval(content_stripped)
                if isinstance(parsed, list):
                    return _extract_text(parsed)
            except (ValueError, SyntaxError):
                pass
        return content

    # Anthropic-style list of content blocks
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif hasattr(block, "text"):          # pydantic model variant
                parts.append(block.text)
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts).strip()

    # Fallback: coerce to string
    return str(content)


async def generation_node(state: RAGState) -> dict:
    llm = get_llm(state["metadata"]["llm_provider"])

    # Check if the query is routed directly (conversational/greetings)
    if state.get("route") == "direct":
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful, polite, and friendly assistant. Answer the user's query directly and conversationally."),
            ("human", "{query}")
        ])
        chain = prompt | llm
        answer = chain.invoke({"query": state["rewritten_query"]})
        return {"answer": _extract_text(answer.content)}

    # Standard vector store document-grounded query
    prompt = await PromptRegistry.get(state["metadata"]["prompt_version"])
    chain = prompt | llm
    answer = chain.invoke({
        "query":    state["rewritten_query"],
        "contexts": "\n\n".join(state["contexts"]),
    })
    return {"answer": _extract_text(answer.content)}