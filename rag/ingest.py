import os
from pathlib import Path
import logging
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import ollama

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Ingestor:
    def __init__(self, qdrant_url="http://localhost:6333", collection_name="disaster_guidelines"):
        self.client = QdrantClient(url=qdrant_url)
        self.collection_name = collection_name
        self._setup_collection()

    def _setup_collection(self):
        # Create collection if it doesn't exist
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)

        if not exists:
            logger.info(f"Creating collection {self.collection_name}...")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE), # nomic-embed-text size
            )

    def get_embeddings(self, text):
        response = ollama.embeddings(model="nomic-embed-text", prompt=text)
        return response["embedding"]

    def process_folder(self, folder_path: str):
        path = Path(folder_path)
        if not path.exists():
            logger.error(f"Knowledge folder {folder_path} not found.")
            return

        # Splitter for chunking
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        files = list(path.glob("*.pdf")) + list(path.glob("*.txt"))
        logger.info(f"Processing {len(files)} documents...")

        for file in files:
            text = ""
            if file.suffix == ".pdf":
                reader = PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            else:
                text = file.read_text(encoding="utf-8")

            chunks = splitter.split_text(text)

            # Vectorize and upload
            points = []
            for i, chunk in enumerate(chunks):
                vector = self.get_embeddings(chunk)
                points.append(PointStruct(
                    id=hash(f"{file.name}_{i}"),
                    vector=vector,
                    payload={"text": chunk, "source": file.name}
                ))

            self.client.upsert(collection_name=self.collection_name, points=points)
            logger.info(f"Ingested {len(chunks)} chunks from {file.name}")

if __name__ == "__main__":
    # Run ingestion from knowledge folder
    ingestor = Ingestor()
    ingestor.process_folder("knowledge")
