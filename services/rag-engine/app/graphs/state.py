from typing import TypedDict, Annotated
from operator import add

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