# 🚀 Deployment Guide

## System Requirements
- Docker and Docker Compose installed.
- NVIDIA GPU with NVIDIA Container Toolkit (Highly recommended for AI performance).

## Quick Start
1. **Prepare Environment**:
   ```bash
   cp .env.example .env
   ```

2. **Launch the System**:
   ```bash
   docker compose up --build -d
   ```

3. **Verify Services**:
   - Frontend: `http://localhost:5173`
   - Backend API: `http://localhost:8000/docs`
   - RAG Service: `http://localhost:8001`

## Troubleshooting
- **Ollama Models**: The `rag` container pulls models on startup. If the RAG service is slow, check `docker compose logs rag`.
- **Database**: If the backend fails to start, ensure the `db` container is healthy (`docker compose ps`).
- **Weights**: Ensure `ai/models/weights/best.pt` is present before starting the backend.
