# syntax=docker/dockerfile:1
# --- Builder: install the package into an isolated venv ------------------
FROM python:3.12-slim AS builder

ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml ./
COPY src ./src
RUN pip install .

# --- Runtime -------------------------------------------------------------
FROM python:3.12-slim AS runtime

ENV PYTHONUNBUFFERED=1 PATH="/opt/venv/bin:$PATH"
WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY alembic.ini ./
COPY alembic ./alembic
COPY scripts ./scripts
COPY docker/entrypoint.sh ./entrypoint.sh

RUN chmod +x ./entrypoint.sh \
    && useradd --create-home --uid 1000 app \
    && chown -R app:app /app
USER app

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
