import os

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter


def setup_otel() -> None:
    service_name = os.getenv("OTEL_SERVICE_NAME", "otelTest-api")
    endpoint = os.environ["SIGNOZ_OTLP_ENDPOINT"]

    resource = Resource.create(
        {
            "service.name": service_name,
            "deployment.environment": os.getenv("DEPLOYMENT_ENV", "dev"),
            "service.version": os.getenv("SERVICE_VERSION", "0.0.0"),
        }
    )

    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    exporter = OTLPSpanExporter(
        endpoint=f"{endpoint}/v1/traces",
        timeout=10,
    )
    provider.add_span_processor(BatchSpanProcessor(exporter))
