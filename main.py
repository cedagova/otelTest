from fastapi import FastAPI

app = FastAPI(title="otelTest API")


@app.get("/healthz")
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
