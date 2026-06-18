from app.llm.factory import get_llm
from app.state import RAGState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

async def rewrite_query_node(state: RAGState) -> dict:
    # Check if we should rewrite or keep original
    query = state.get("query", "")
    provider = state["metadata"].get("llm_provider", "gemini")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an advanced query optimizer. Your job is to rewrite the input user query to make it better suited for vector database semantic search. "
                   "Resolve any pronoun references (like 'he', 'they', 'it'), expand synonyms, and strip conversational fluff (like 'please', 'can you tell me'). "
                   "Output ONLY the optimized query text, and absolutely nothing else."),
        ("human", "Optimize this query: {query}")
    ])
    
    try:
        llm = get_llm(provider, temperature=0)
        chain = prompt | llm | StrOutputParser()
        rewritten = chain.invoke({"query": query})
        rewritten = rewritten.strip()
        # Fallback if empty
        if not rewritten:
            rewritten = query
        return {"rewritten_query": rewritten}
    except Exception as e:
        print(f"Query rewriting failed: {e}. Using original query.")
        return {"rewritten_query": query}

async def route_query_node(state: RAGState) -> dict:
    query = state.get("query", "")
    provider = state["metadata"].get("llm_provider", "gemini")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a query router. Your job is to classify if the user query requires retrieving information from uploaded documents or if it is generic/conversational. "
                   "Respond strictly with 'vectorstore' if the query asks about files, resumes, text chunks, specific documents, projects, or facts that need database lookup. "
                   "Respond strictly with 'direct' if the query is a simple greeting ('hi', 'hello'), a polite comment, general knowledge, or conversational chatter that requires no document context. "
                   "Output ONLY either 'vectorstore' or 'direct', and nothing else."),
        ("human", "Route this query: {query}")
    ])
    
    try:
        llm = get_llm(provider, temperature=0)
        chain = prompt | llm | StrOutputParser()
        route = chain.invoke({"query": query})
        route = route.strip().lower()
        if "direct" in route:
            final_route = "direct"
        else:
            final_route = "vectorstore"
        return {"route": final_route}
    except Exception as e:
        print(f"Query routing failed: {e}. Defaulting to vectorstore.")
        return {"route": "vectorstore"}
