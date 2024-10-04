FROM python:3.12-alpine3.20 AS builder
RUN apk add --no-cache build-base
RUN pip install poetry==1.8.3
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi

FROM python:3.12-alpine3.20 AS runtime
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app:$PYTHONPATH"
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY . .
CMD ["python", "conversation_agent/app.py", "run", "--host=0.0.0.0", "--port=5000", "--env-file=.env"]
EXPOSE 5000