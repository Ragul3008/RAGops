class PromptRecord:
    def __init__(self, messages: list):
        self.messages = messages

class PgPromptStore:
    """In-memory fallback for PgPromptStore to load system prompts."""
    
    def __init__(self):
        self.prompts = {
            "v1": PromptRecord([
                ("system", "You are a helpful fact-based assistant. Answer the query ONLY using the provided context. If the context is empty, does not contain the answer, or if you cannot find the answer in the context, respond strictly with: 'I do not have the context to answer this query.'\n\nContext:\n{contexts}"),
                ("human", "{query}")
            ])
        }

    async def get(self, version: str) -> PromptRecord:
        if version not in self.prompts:
            return self.prompts["v1"]
        return self.prompts[version]

    async def create(self, messages: list, metadata: dict) -> str:
        version_id = f"v_{len(self.prompts) + 1}"
        self.prompts[version_id] = PromptRecord(messages)
        return version_id
