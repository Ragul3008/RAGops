import asyncio
import numpy as np
from app.retrieval.factory import get_retriever
from app.embedding.factory import get_embedder
from app.state import RAGState
from app.llm.factory import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

_cross_encoder_cache = {}

def get_cross_encoder(model_name: str = "cross-encoder/ms-marco-MiniLM-L-2-v2"):
    global _cross_encoder_cache
    if model_name not in _cross_encoder_cache:
        from sentence_transformers import CrossEncoder
        _cross_encoder_cache[model_name] = CrossEncoder(model_name, device="cpu")
    return _cross_encoder_cache[model_name]

async def retrieval_node(state: RAGState) -> dict:
    metadata = state["metadata"]
    original_query = state.get("query", "")
    rewritten_query = state.get("rewritten_query", original_query)
    
    embedder = get_embedder(metadata)
    retriever = get_retriever(metadata)
    
    # 1. Determine queries to embed and retrieve
    queries = [rewritten_query]
    
    enable_multi_query = metadata.get("multi_query", False)
    if enable_multi_query:
        print(f"[ADVANCED RAG] Multi-Query expansion enabled for query: {original_query}")
        try:
            llm_provider = metadata.get("llm_provider", "gemini")
            llm = get_llm(llm_provider, temperature=0)
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an advanced query expansion assistant. Your task is to generate 3 alternative versions of the input user query to help retrieve matching context from a vector store. "
                           "Each variation should capture a different perspective or expand synonyms. "
                           "Respond with exactly 3 optimized queries, one per line. Do not number them, and output nothing else."),
                ("human", "Generate 3 variations for: {query}")
            ])
            chain = prompt | llm | StrOutputParser()
            res = await chain.ainvoke({"query": original_query})
            variations = [line.strip() for line in res.strip().split("\n") if line.strip()]
            if variations:
                queries.extend(variations[:3])
                print(f"[ADVANCED RAG] Expanded queries: {queries}")
        except Exception as e:
            print(f"[ADVANCED RAG] Multi-Query expansion failed: {e}. Using optimized query only.")
            
    # 2. Retrieve documents in parallel for all queries
    async def retrieve_for_query(q):
        try:
            q_vec = await embedder.embed_query(q)
            docs = await retriever.retrieve(
                query_vector=q_vec,
                tenant_id=metadata["tenant_id"],
                top_k=metadata.get("top_k", 5),
                score_threshold=metadata.get("score_threshold", 0.7)
            )
            return docs
        except Exception as err:
            print(f"Retrieval failed for query '{q}': {err}")
            return []

    # Run in parallel
    retrieved_results = await asyncio.gather(*(retrieve_for_query(q) for q in queries))
    
    # Flatten and deduplicate by content
    seen_content = set()
    unique_docs = []
    for docs in retrieved_results:
        for d in docs:
            content = d["content"]
            if content not in seen_content:
                seen_content.add(content)
                unique_docs.append(d)
                
    # 3. Apply Re-ranking if enabled
    enable_reranking = metadata.get("rerank", False)
    
    if enable_reranking and unique_docs:
        print(f"[ADVANCED RAG] Cross-Encoder Re-ranking enabled for {len(unique_docs)} unique contexts.")
        try:
            model = get_cross_encoder()
            pairs = [[original_query, doc["content"]] for doc in unique_docs]
            
            # Predict scores using executor to avoid blocking event loop
            loop = asyncio.get_event_loop()
            scores = await loop.run_in_executor(None, lambda: model.predict(pairs))
            
            # Associate scores and sort
            scored_docs = list(zip(unique_docs, scores))
            scored_docs.sort(key=lambda x: x[1], reverse=True)
            
            # Print ranked results for debugging
            print("[ADVANCED RAG] Re-ranked results:")
            for idx, (doc, score) in enumerate(scored_docs):
                print(f"  Rank #{idx+1} (Score: {score:.4f}): {doc['content'][:80]}...")
                
            unique_docs = [doc for doc, score in scored_docs]
        except Exception as e:
            print(f"[ADVANCED RAG] Re-ranking failed: {e}. Proceeding with standard retrieval order.")

    final_contexts = [doc["content"] for doc in unique_docs]
    top_k = metadata.get("top_k", 5)
    
    return {
        "contexts":  final_contexts[:top_k],
        "iteration": state.get("iteration", 0) + 1,
    }