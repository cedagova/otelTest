from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

from oteltest.otel import setup_otel

setup_otel()

tracer = trace.get_tracer(__name__, "1.0.0")

app = FastAPI(title="otelTest API")

# auto-instrument incoming requests + outgoing requests
# excluded_urls is matched against the full URL (e.g. http://host:port/health), not just the path
FastAPIInstrumentor.instrument_app(app, excluded_urls=r".*/health/?$")
# RequestsInstrumentor().instrument()


@app.get("/health")
def health():
    """Check that the API is up."""
    return {"status": "ok", "message": "API is up"}


@app.get("/traces")
def traces():
    """Run a mocked process (network, db, business logic) and emit a trace for telemetry."""
    from oteltest.mocked_process import run_mocked_process

    run_mocked_process(tracer)
    return {"status": "ok", "message": "Mocked process completed; check your telemetry backend for the trace."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
