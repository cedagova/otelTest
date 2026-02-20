FROM python:3.12-slim

WORKDIR /app

# Install poetry (no venv in container)
ENV POETRY_VERSION=1.8.5 \
    POETRY_VIRTUALENVS_CREATE=false
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-interaction --no-ansi

COPY main.py .

# Render sets PORT at runtime (e.g. 10000); default 8000 for local
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
