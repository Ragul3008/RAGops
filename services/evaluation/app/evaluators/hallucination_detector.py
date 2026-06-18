from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class HallucinationDetector:
    """Detects hallucinations via NLI-style
    faithfulness checking using an LLM judge."""
    
    PROMPT = ChatPromptTemplate.from_messages([
        ("system", """You are a strict fact-checker.
Given context and an answer, determine if the
answer contains ONLY information from the context.
Respond with JSON: {{"hallucinated": bool,
"evidence": str, "confidence": float}}"""),
        ("human", "Context:\n{context}\nAnswer:\n{answer}")
    ])
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.chain = self.PROMPT | self.llm

    async def detect(
        self, answer: str, contexts: list[str]
    ) -> HallucinationResult:
        context = "\n---\n".join(contexts)
        result = await self.chain.ainvoke({
            "context": context,
            "answer":  answer,
        })
        return HallucinationResult.parse_raw(
            result.content
        )