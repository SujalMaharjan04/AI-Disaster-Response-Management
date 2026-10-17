# AI-Powered Disaster Response Management (Nepal)

An AI-powered platform for analyzing disaster satellite imagery to provide actionable emergency recommendations for Nepal.

## 🚀 Core Features
- **AI Damage Assessment**: YOLO-based segmentation to identify building damage (No Damage, Minor, Major, Destroyed).
- **RAG-Powered Recommendations**: Local LLM (Ollama) using disaster response guidelines to provide emergency advice based on AI findings.
- **Interactive Dashboard**: Leaflet-based map for visualizing damage and recommendations.

## 🛠 Tech Stack
- **AI/ML**: PyTorch, YOLOv11/v8, OpenCV, NumPy.
- **Backend**: FastAPI, PostgreSQL, SQLAlchemy, WebSockets.
- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Leaflet.
- **RAG**: Ollama (Qwen 2.5), Qdrant, Sentence Transformers.
- **Infra**: Docker, UV (Python package manager).

## 📂 Project Structure
- `ai/`: Training pipeline, preprocessing, and inference.
- `backend/`: FastAPI server and database logic.
- `frontend/`: React dashboard.
- `rag/`: Local LLM integration and vector DB.
- `knowledge/`: Local documents for RAG.
- `data/`: raw and processed datasets (not committed).
- `docker/`: Containerization config.

## 🏁 Getting Started

### Prerequisites
- Docker & Docker Compose
- UV (installed via `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- NVIDIA GPU (Optional, for local inference)

### Setup
1. Clone the repo: `git clone <repo-url>`
2. Set up environment: `cp .env.example .env`
3. Run the system: `docker compose up --build`

## 🗺 Roadmap
- [ ] Phase 0: Repo Setup (Current)
- [ ] Phase 1: Dataset Exploration
- [ ] Phase 2: Preprocessing
- [ ] Phase 3: Colab Training
- [ ] Phase 4: Local Inference
- [ ] Phase 5: FastAPI Backend
- [ ] Phase 6: RAG Implementation
- [ ] Phase 7: Frontend Development
- [ ] Phase 8: Integration & Deployment
