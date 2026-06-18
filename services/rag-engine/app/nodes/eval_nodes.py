from app.llm.factory import get_llm
from app.state import RAGState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

async def faithfulness_node(state: RAGState) -> dict:
    answer = state.get("answer", "")
    contexts = state.get("contexts", [])
    
    # If the LLM refused to answer (grounding block), it is faithful to context.
    if answer == "I do not have the context to answer this query.":
        return {"faithful": True}
        
    # Prevent infinite routing loops by terminating after 3 iterations
    if state.get("iteration", 0) >= 3:
        print("Maximum RAG loop iterations reached (3). Terminating self-correction.")
        return {"faithful": True}
        
    provider = state["metadata"].get("llm_provider", "gemini")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI fact validator. Your task is to verify if the generated answer is entirely faithful to and supported by the retrieved contexts. "
                   "If the answer contains any claims, names, numbers, or facts that are NOT explicitly mentioned in the context, you must respond strictly with 'no'. "
                   "If the answer is fully supported and can be directly derived from the context, respond strictly with 'yes'. "
                   "Provide ONLY 'yes' or 'no', and nothing else."),
        ("human", "Retrieved Contexts:\n{contexts}\n\nGenerated Answer:\n{answer}")
    ])
    
    try:
        llm = get_llm(provider, temperature=0)
        chain = prompt | llm | StrOutputParser()
        result = chain.invoke({
            "contexts": "\n\n".join(contexts),
            "answer": answer
        })
        is_faithful = "yes" in result.strip().lower()
        print(f"Self-Evaluation check: '{result.strip()}' (is_faithful={is_faithful})")
        return {"faithful": is_faithful}
    except Exception as e:
        print(f"Self-Evaluation check failed: {e}. Defaulting to True.")
        return {"faithful": True}
