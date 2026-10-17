import logging
import requests
from pathlib import Path
from typing import Dict, Any
from sqlalchemy.orm import Session
from . import models
from ai.inference.engine import InferenceEngine

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        # Initialize the model engine
        self.engine = InferenceEngine()
        # RAG service URL (defined in docker-compose)
        self.rag_url = "http://rag:8001/recommend"

    async def process_image(self, db: Session, request_id: int, file_path: str):
        """
        Wraps the inference engine to process an image and get RAG recommendations.
        """
        try:
            # Update status to processing
            request = db.query(models.AnalysisRequest).filter(models.AnalysisRequest.id == request_id).first()
            if request:
                request.status = "processing"
                db.commit()

            # 1. AI Inference: Get damage counts
            result = self.engine.predict(file_path)

            # 2. RAG: Generate recommendation based on counts
            recommendation = "No recommendation available."
            try:
                rag_resp = requests.post(
                    self.rag_url,
                    json={"damage_summary": result["damage_summary"]},
                    timeout=30
                )
                if rag_resp.status_code == 200:
                    recommendation = rag_resp.json().get("recommendation", recommendation)
            except Exception as rag_e:
                logger.error(f"RAG service error: {rag_e}")

            # 3. Save Report to DB
            report = models.DamageReport(
                request_id=request_id,
                total_buildings=result["damage_summary"]["total_buildings"],
                destroyed=result["damage_summary"]["destroyed"],
                major_damage=result["damage_summary"]["major_damage"],
                minor_damage=result["damage_summary"]["minor_damage"],
                no_damage=result["damage_summary"]["no_damage"],
                confidence=result["confidence"]
            )

            if request:
                request.status = "completed"

            db.add(report)
            db.commit()

            # Append recommendation to the result for the frontend
            result["recommendation"] = recommendation

            return result

        except Exception as e:
            logger.error(f"Error processing request {request_id}: {e}")
            request = db.query(models.AnalysisRequest).filter(models.AnalysisRequest.id == request_id).first()
            if request:
                request.status = "failed"
                db.commit()
            raise e

# Singleton instance
ai_service = AIService()
