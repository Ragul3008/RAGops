import socket

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor
)

# Attempt to load exporters, fallback if blocked by DLL loading restrictions (cygrpc)
try:
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
        OTLPSpanExporter
    )
except Exception:
    try:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter
        )
    except Exception:
        try:
            from opentelemetry.sdk.trace.export import ConsoleSpanExporter as OTLPSpanExporter
        except Exception:
            OTLPSpanExporter = None

from opentelemetry.instrumentation.fastapi import (
    FastAPIInstrumentor
)

def is_otlp_reachable() -> bool:
    """Check if the OTLP collector port is open on localhost to avoid blocking timeouts."""
    for port in [4317, 4318]:
        try:
            s = socket.create_connection(("127.0.0.1", port), timeout=0.1)
            s.close()
            return True
        except Exception:
            continue
    return False

def setup_otel(app, service_name: str):
    if not is_otlp_reachable():
        print(f"OTLP collector is not reachable on port 4317/4318. Telemetry is disabled for {service_name}.")
        return
        
    if OTLPSpanExporter is None:
        print(f"Skipping OTLP telemetry setup for {service_name} due to missing exporter (cygrpc block).")
        return
    try:
        provider = TracerProvider()
        provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter())
        )
        trace.set_tracer_provider(provider)
        FastAPIInstrumentor.instrument_app(app)
    except Exception as e:
        print(f"Failed to setup telemetry for {service_name}: {e}. Continuing without telemetry.")