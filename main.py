from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

from oteltest.otel import setup_otel

setup_otel()

app = FastAPI(title="otelTest API")

# auto-instrument incoming requests + outgoing requests
FastAPIInstrumentor.instrument_app(app, excluded_urls=r"^/health/?$")
RequestsInstrumentor().instrument()


@app.get("/health")
def healthz():
    """Check that the API is up."""
    return {"status": "ok", "message": "API is up"}


@app.get("/traces")
def traces():
    """Traces endpoint — logic to be defined later."""
    # TODO: add traces logic
    return {"traces": []}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
