import logging
import os
import httpx

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

from oteltest.otel import setup_otel

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
)
setup_otel()

tracer = trace.get_tracer(__name__, "1.0.0")

app = FastAPI(title="otelTest API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chunipers.com","https://www.chunipers.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# auto-instrument incoming requests + outgoing requests
# excluded_urls is matched against the full URL (e.g. http://host:port/health), not just the path
FastAPIInstrumentor.instrument_app(app, excluded_urls=r".*/health/?$")
RequestsInstrumentor().instrument()


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

MAX_BODY = 2 * 1024 * 1024  # 2MB


@app.options("/v1/traces")
async def traces_preflight():
    return Response(status_code=204)


@app.post("/v1/traces")
async def receive_traces(request: Request):
    endpoint = os.getenv("OTEL_COLLECTOR_ENDPOINT")
    if not endpoint:
        raise RuntimeError("OTEL_COLLECTOR_ENDPOINT not set")

    body = await request.body()
    if len(body) > MAX_BODY:
        return JSONResponse(status_code=413, content={"error": "payload too large"})

    content_type = request.headers.get("content-type", "application/x-protobuf")
    forward_url = f"{endpoint.rstrip('/')}/v1/traces"

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(
                forward_url,
                content=body,
                headers={"Content-Type": content_type},
            )
        return Response(status_code=r.status_code)
    except Exception:
        logging.getLogger(__name__).exception("Failed to forward traces")
        return JSONResponse(status_code=502, content={"error": "forward failed"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
