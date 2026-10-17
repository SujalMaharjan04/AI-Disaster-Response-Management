from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class AnalysisRequest(Base):
    __tablename__ = "analysis_requests"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    status = Column(String, default="pending") # pending, processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)

    report = relationship("DamageReport", back_populates="request", uselist=False)

class DamageReport(Base):
    __tablename__ = "damage_reports"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("analysis_requests.id"))
    total_buildings = Column(Integer)
    destroyed = Column(Integer)
    major_damage = Column(Integer)
    minor_damage = Column(Integer)
    no_damage = Column(Integer)
    confidence = Column(Float)

    request = relationship("AnalysisRequest", back_populates="report")
