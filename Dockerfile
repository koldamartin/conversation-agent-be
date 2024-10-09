FROM python:3.12-alpine3.20 AS builder

# Combine RUN commands and clean up in the same layer
RUN apk add --no-cache build-base \
    && pip install --no-cache-dir poetry==1.8.3 \
    && rm -rf /root/.cache/pip

# Set environment variables
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Copy only necessary files for dependency installation
COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir flask-sqlalchemy

# Install dependencies and remove cache in the same layer
RUN poetry install --no-dev --no-interaction --no-ansi \
    && rm -rf $POETRY_CACHE_DIR

FROM python:3.12-alpine3.20 AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app:$PYTHONPATH"

WORKDIR /app

# Copy only the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy only necessary files for the application
COPY conversation_agent ./conversation_agent

RUN pip install --no-cache-dir gunicorn

# Run the application based on the environment
CMD if [ "$ENVIRONMENT" = "production" ]; then gunicorn -w 4 -b 0.0.0.0:8080 -t 300 conversation_agent.app:app;else python conversation_agent/app.py run --host=0.0.0.0 --port=5000 --env-file=.env; fi

EXPOSE ${PORT}