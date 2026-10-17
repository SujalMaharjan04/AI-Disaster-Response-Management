# Build stage for Python dependencies
FROM python:3.11-slim as builder

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-install-project

# Final stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY backend/ /app/
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["uv", "run", "python", "-m", "app.main"]
