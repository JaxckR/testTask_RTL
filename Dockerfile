FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
WORKDIR /app

COPY ./pyproject.toml ./pyproject.toml
COPY ./README.md ./alembic.ini ./llm_prompt.txt ./
COPY ./videos.json ./scripts ./
COPY ./src ./src

RUN uv pip install --system --target dependencies .

FROM python:3.12-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/app/dependencies"

COPY --from=builder /app/ ./
