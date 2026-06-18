from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

@dataclass
class DomainEvent:
    event_id:   UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(
        default_factory=datetime.utcnow
    )

@dataclass
class DocumentIngested(DomainEvent):
    tenant_id:    str = ""
    document_id:  str = ""
    chunk_count:  int = 0
    vector_store: str = ""

@dataclass
class EvaluationCompleted(DomainEvent):
    run_id:     str = ""
    tenant_id:  str = ""
    scores:     dict = field(default_factory=dict)

@dataclass
class HallucinationDetected(DomainEvent):
    query_id:   str = ""
    tenant_id:  str = ""
    confidence: float = 0.0