
class GEvalEvaluator:
    """G-Eval: LLM-as-judge evaluation using
    chain-of-thought scoring for nuanced quality
    assessment beyond RAGAS metrics."""
    
    CRITERIA = {
        "coherence":    "Is the answer coherent?",
        "fluency":      "Is the language fluent?",
        "relevance":    "Is it relevant to the question?",
        "completeness": "Does it fully answer the question?",
    }
    
    async def evaluate(
        self, question: str, answer: str,
        criteria: list[str] | None = None,
    ) -> dict[str, float]:
        criteria = criteria or list(self.CRITERIA)
        scores = {}
        for c in criteria:
            scores[c] = await self._score(
                question, answer, c
            )
        return scores