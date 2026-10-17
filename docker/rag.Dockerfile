# RAG environment setup
FROM python:3.11-slim
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY rag/pyproject.toml rag/uv.lock ./
RUN uv sync --frozen
COPY rag/ /app/
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8001
CMD ["uv", "run", "python", "-m", "rag.main"]
