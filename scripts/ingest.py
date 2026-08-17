"""
scripts/ingest.py - run this once (or any time you edit the data/documents/ folder) to
build FitMind AI's knowledge base: Ingestion & Chunking -> Embeddings -> Vector DB.

Run from the project root:
    python -m scripts.ingest
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.chunking import build_all_chunks
from src.core.vector_store import build_collection


def main():
    print("Step 1/2 — Ingestion & Chunking (one strategy per FitMind knowledge type):")
    chunks = build_all_chunks()
    print(f"\nTotal chunks: {len(chunks)}")

    print("\nStep 2/2 — Embedding + Vector DB indexing (Qdrant, local/embedded, HNSW index)...")
    count = build_collection(chunks)
    print(f"Indexed {count} chunks into Qdrant collection at ./qdrant_data")
    print("\nFitMind AI's knowledge base is ready.")
    print("Start the API:  uvicorn src.api.main:app --reload --port 8000")
    print("Start the UI:   streamlit run src/ui/streamlit_app.py")


if __name__ == "__main__":
    main()
