from langgraph.graph import StateGraph, END
from app.nodes.query_nodes import (
    rewrite_query_node,
    route_query_node,
)
from app.nodes.retrieval_nodes import retrieval_node
from app.nodes.generation_nodes import generation_node
from app.nodes.eval_nodes import faithfulness_node
from app.state import RAGState

def build_rag_graph() -> StateGraph:
    graph = StateGraph(RAGState)
    
    graph.add_node("rewrite_query",   rewrite_query_node)
    graph.add_node("route_query",     route_query_node)
    graph.add_node("retrieve",        retrieval_node)
    graph.add_node("generate",        generation_node)
    graph.add_node("check_faithfulness", faithfulness_node)
    
    graph.set_entry_point("rewrite_query")
    graph.add_edge("rewrite_query", "route_query")
    graph.add_conditional_edges(
        "route_query",
        lambda s: s["route"],
        {"vectorstore": "retrieve", "direct": "generate"}
    )
    graph.add_edge("retrieve", "generate")
    graph.add_conditional_edges(
        "generate",
        lambda s: "end" if s.get("route") == "direct" else "check_faithfulness",
        {"end": END, "check_faithfulness": "check_faithfulness"}
    )
    graph.add_conditional_edges(
        "check_faithfulness",
        lambda s: "end" if s["faithful"] else "retrieve",
        {"end": END, "retrieve": "retrieve"}
    )
    return graph.compile()