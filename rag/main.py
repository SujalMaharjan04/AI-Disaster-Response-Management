from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .engine import RAGEngine

app = FastAPI(title="RAG Recommendation Service")
rag_engine = RAGEngine()

class RecommendationRequest(BaseModel):
    damage_summary: dict

class RecommendationResponse(BaseModel):
    recommendation: str

@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendation(request: RecommendationRequest):
    try:
        recommendation = rag_engine.generate_recommendation(request.damage_summary)
        return {"recommendation": recommendation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
