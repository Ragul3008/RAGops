from prometheus_client import (
    Counter, Histogram, Gauge, Summary
)

# Request metrics
http_requests = Counter(
    "ragops_http_requests_total",
    "Total HTTP requests",
    ["service","method","endpoint","status"],
)
request_duration = Histogram(
    "ragops_request_duration_seconds",
    "Request latency",
    ["service","endpoint"],
    buckets=[0.01,0.05,0.1,0.25,0.5,1,2.5,5,10],
)

# RAG-specific metrics
rag_retrieval_latency = Histogram(
    "ragops_retrieval_latency_seconds",
    "Retrieval stage latency",
    ["tenant_id","strategy"],
)
rag_generation_latency = Histogram(
    "ragops_generation_latency_seconds",
    "LLM generation latency",
    ["tenant_id","provider","model"],
)
rag_hallucination_rate = Gauge(
    "ragops_hallucination_rate",
    "Rolling hallucination detection rate",
    ["tenant_id","project_id"],
)

# Cost metrics
llm_token_cost = Counter(
    "ragops_llm_cost_usd_total",
    "Cumulative LLM cost in USD",
    ["tenant_id","provider","model"],
)
embedding_cost = Counter(
    "ragops_embedding_cost_usd_total",
    "Cumulative embedding cost in USD",
    ["tenant_id","provider"],
)