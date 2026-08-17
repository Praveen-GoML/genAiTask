"""
src/core/rag.py - the RAG pipeline: Retrieval & Context Injection, then Generation.

This module ONLY answers questions using retrieved context — it never takes an action.
That's the deliberate RAG-vs-Agentic distinction preserved from the architecture design.
"""

from src.core.vector_store import retrieve
from src.core.llm import chat
from config.settings import settings

FITMIND_SYSTEM_PROMPT = settings.FITMIND_SYSTEM_PROMPT
TOP_K = settings.TOP_K


def format_context(chunks: list) -> str:
    """Context injection: format retrieved chunks with clear source labels so the model
    can cite which knowledge area answered — avoids the 'dump everything in' mistake."""
    if not chunks:
        return "No relevant information found in the FitMind knowledge base."
    lines = []
    for i, c in enumerate(chunks, 1):
        lines.append(f"[{i}] (source: {c['doc_type']}) {c['text']}")
    return "\n".join(lines)


def answer(query: str, top_k: int = TOP_K, history: list = None):
    """Retrieval & Context Injection -> Generation.
    Returns (reply_text, retrieved_chunks) — chunks let the caller show which sources
    were used."""
    chunks = retrieve(query, top_k=top_k)
    context = format_context(chunks)

    messages = [{"role": "system", "content": FITMIND_SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({
        "role": "user",
        "content": (
            f"CONTEXT:\n{context}\n\n"
            f"QUESTION: {query}\n\n"
            "Answer using ONLY the context above."
        ),
    })

    reply = chat(messages)
    return reply, chunks
