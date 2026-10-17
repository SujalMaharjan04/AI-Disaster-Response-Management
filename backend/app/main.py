from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import endpoints
from .database import Base, engine
from .api.endpoints import router as api_router

# Initialize Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Disaster Response Backend",
    description="Backend for analyzing disaster satellite imagery and providing recommendations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routes
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Disaster Response Management API"}
