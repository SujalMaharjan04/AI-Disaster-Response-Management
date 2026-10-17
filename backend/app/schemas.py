from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DamageSummary(BaseModel):
    total_buildings: int
    destroyed: int
    major_damage: int
    minor_damage: int
    no_damage: int

class AnalysisResponse(BaseModel):
    location: str
    damage_summary: DamageSummary
    confidence: float

class RequestStatus(BaseModel):
    request_id: int
    status: str
    filename: str
    created_at: datetime
