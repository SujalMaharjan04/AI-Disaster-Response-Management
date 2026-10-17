#!/bin/bash
set -e

echo "Waiting for database to be ready..."
until pg_isready -h db -p 5432; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "Starting FastAPI backend..."
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
