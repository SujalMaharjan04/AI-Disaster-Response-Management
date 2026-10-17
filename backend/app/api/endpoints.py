from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database
from .services.ai_service import ai_service
import shutil
from pathlib import Path
import uuid
import asyncio

router = APIRouter()
UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Simple in-memory manager for WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_message(self, client_id: str, message: dict):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)

manager = ConnectionManager()

@router.post("/upload", response_model=schemas.RequestStatus)
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    # 1. Save file to disk
    file_ext = Path(file.filename).suffix
    unique_name = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_name

    with file.file as buffer:
        shutil.copyfileobj(buffer, open(file_path, "wb"))

    # 2. Create analysis request in DB
    request = models.AnalysisRequest(filename=unique_name)
    db.add(request)
    db.commit()
    db.refresh(request)

    # 3. Trigger AI processing in background
    # We use asyncio.create_task to avoid blocking the response
    asyncio.create_task(process_and_notify(db, request.id, str(file_path)))

    return request

async def process_and_notify(db, request_id, file_path):
    """
    Background task to process AI inference and notify client via WS.
    """
    try:
        # Use a new session for the background task
        with database.SessionLocal() as session:
            result = await ai_service.process_image(session, request_id, file_path)

            # Notify via WebSocket if client is connected
            # We use the request_id as a simple client_id for this demo
            await manager.send_message(str(request_id), {
                "event": "analysis_completed",
                "request_id": request_id,
                "data": result
            })
    except Exception as e:
        print(f"Background processing failed: {e}")

@router.get("/results/{request_id}", response_model=schemas.AnalysisResponse)
async def get_results(request_id: int, db: Session = Depends(database.get_db)):
    request = db.query(models.AnalysisRequest).filter(models.AnalysisRequest.id == request_id).first()
    if not request or not request.report:
        raise HTTPException(status_code=404, detail="Analysis not completed or not found")

    report = request.report
    return {
        "location": request.filename,
        "damage_summary": {
            "total_buildings": report.total_buildings,
            "destroyed": report.destroyed,
            "major_damage": report.major_damage,
            "minor_damage": report.minor_damage,
            "no_damage": report.no_damage
        },
        "confidence": report.confidence
    }

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)
    try:
        while True:
            # Keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(client_id)
