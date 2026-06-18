from decimal import Decimal
from app.models.usage import UsageRecord
from app.infrastructure.repositories import (
    IUsageRepository
)

PRICING = {
    "openai": {
        "gpt-4o":       {"input": 5.0,   "output": 15.0},
        "gpt-4o-mini":  {"input": 0.15,  "output": 0.6},
        "gpt-3.5-turbo":{"input": 0.5,   "output": 1.5},
    },
    "anthropic": {
        "claude-3-5-sonnet-20241022": {
            "input": 3.0, "output": 15.0
        },
    },
}

class CostTracker:
    def __init__(self, repo: IUsageRepository):
        self.repo = repo

    async def record(
        self, tenant_id: str, provider: str,
        model: str, input_tokens: int,
        output_tokens: int,
    ) -> Decimal:
        p = PRICING[provider][model]
        cost = Decimal(
            (input_tokens  * p["input"] +
             output_tokens * p["output"]) / 1_000_000
        )
        await self.repo.save(UsageRecord(
            tenant_id=tenant_id,
            provider=provider, model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
        ))
        return cost