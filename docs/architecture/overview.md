# RAGOps Architecture Overview

## Design Principles
- Domain-Driven Design with Bounded Contexts
- Clean Architecture (domain → application → infra)
- Event-Driven with domain events via Kafka
- CQRS for read/write separation at scale
- Zero Trust Security (mTLS, JWT, RBAC)
- Multi-tenant via PostgreSQL RLS

## Bounded Contexts
1. Identity & Access (auth, users, orgs, RBAC)
2. RAG Core (projects, documents, pipelines)
3. AI Infrastructure (embeddings, vectors, LLMs)
4. Evaluation (metrics, hallucination, quality)
5. Observability (metrics, traces, logs, costs)
6. Billing (usage, limits, subscriptions)

## Data Flow
Upload → S3 → Celery → Parse → Chunk 
→ Embed → Qdrant → [Query] → Retrieve 
→ Rerank → Generate → Evaluate → Cache