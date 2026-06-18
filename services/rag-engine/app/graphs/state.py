from typing import TypedDict

class RAGState(TypedDict):
    query:           str
    rewritten_query: str
    route:           str
    contexts:        list[str]
    answer:          str
    faithful:        bool
    hallucination:   dict
    metadata:        dict
    iteration:       int