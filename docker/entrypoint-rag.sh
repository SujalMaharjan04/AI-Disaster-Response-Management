#!/bin/bash
set -e

# Start Ollama service in background
ollama serve &
sleep 5

echo "Pulling AI models..."
ollama pull nomic-embed-text
ollama pull qwen2.5:7b

echo "Starting knowledge ingestion..."
uv run python ingest.py

echo "RAG system ready."
# Keep container running
tail -f /dev/null
