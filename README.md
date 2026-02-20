# otelTest API

Basic FastAPI app with health check and traces placeholder.

## Setup

```bash
poetry install
```

## Run

```bash
poetry run uvicorn main:app --reload
```

- **GET /test** — health check (API is up)
- **GET /traces** — traces endpoint (logic TBD)

Docs: http://127.0.0.1:8000/docs

## Deploy to Render

1. **Commit everything** (including `poetry.lock` and `render.yaml`).
2. Push the repo to GitHub or GitLab.
3. In [Render Dashboard](https://dashboard.render.com/) → **New** → **Blueprint**.
4. Connect the repo; Render detects `render.yaml` and creates the web service.
5. Deploy; the service will build from the Dockerfile and use `/test` as the health check.
