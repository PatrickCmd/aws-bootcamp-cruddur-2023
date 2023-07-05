from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

# Honeycomb ------------------
# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
# Processor for sending logs to honeycomb
processor = BatchSpanProcessor(OTLPSpanExporter())
# OTEL ----------
# Show this in the logs within the backend-flask app (STDOUT)
simple_console_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
provider.add_span_processor(simple_console_processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)


def init_honeycomb(app):
    """Initialize automatic instrumentation with Flask"""
    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()
