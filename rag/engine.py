import logging
from typing import List
from qdrant_client import QdrantClient
import ollama

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGEngine:
    def __init__(self, qdrant_url="http://localhost:6333", collection_name="disaster_guidelines"):
        self.client = QdrantClient(url=qdrant_url)
        self.collection_name = collection_name
        self.llm_model = "qwen2.5:7b"

    def get_embeddings(self, text):
        response = ollama.embeddings(model="nomic-embed-text", prompt=text)
        return response["embedding"]

    def retrieve_context(self, query: str, top_k=3) -> List[str]:
        # Vectorize query
        vector = self.get_embeddings(query)

        # Search Qdrant
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=top_k
        )

        return [hit.payload["text"] for hit in search_result]

    def generate_recommendation(self, damage_summary: dict) -> str:
        # 1. Create a descriptive query based on AI results
        destroyed = damage_summary["destroyed"]
        major = damage_summary["major_damage"]
        total = damage_summary["total_buildings"]

        query = (
            f"Emergency response guidelines for a disaster area with {total} total buildings, "
            f"{destroyed} destroyed and {major} majorly damaged. "
            f"What are the priority actions for search and rescue and shelter management?"
        )

        # 2. Retrieve relevant context
        context_chunks = self.retrieve_context(query)
        context_text = "\n\n".join(context_chunks)

        # 3. Build Prompt
        prompt = f"""
You are an expert Disaster Response Coordinator for Nepal.
Based on the following official guidelines and the AI-detected damage, provide a concise, actionable emergency recommendation.

OFFICIAL GUIDELINES:
{context_text}

AI DAMAGE SUMMARY:
- Total Buildings: {total}
- Destroyed: {destroyed}
- Major Damage: {major}
- Minor Damage: {damage_summary["minor_damage"]}
- No Damage: {damage_summary["no_damage"]}

INSTRUCTIONS:
1. Be specific and actionable.
2. Prioritize life-saving measures.
3. Use a professional, emergency-response tone.
4. If the guidelines don't provide specific info, use general best practices for disaster response.

RECOMMENDATION:
"""
        # 4. Generate with local LLM
        response = ollama.generate(model=self.llm_model, prompt=prompt)
        return response["response"]
