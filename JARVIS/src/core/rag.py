"""
src/core/rag.py - the RAG pipeline: Retrieval & Context Injection, then Generation & Formatting.

This module ONLY answers questions using retrieved context - it never takes an action.
That's the deliberate RAG-vs-Agentic distinction the course teaches.
"""

from src.core.vector_store import retrieve
from src.core.llm import chat
from config.settings import settings

FRIDAY_SYSTEM_PROMPT = getattr(settings, "FRIDAY_SYSTEM_PROMPT", settings.JARVIS_SYSTEM_PROMPT)
TOP_K = settings.TOP_K


def format_context(chunks):
    """Context injection: format retrieved chunks with clear source labels, so the model
    can (and must) cite which knowledge type answered - and so we avoid the classic
    'dump everything in, hope for the best' mistake from the course."""
    if not chunks:
        return "No relevant information found in F.R.I.D.A.Y.'s knowledge base."
    lines = []
    for i, c in enumerate(chunks, 1):
        lines.append(f"[{i}] (source: {c['doc_type']}) {c['text']}")
    return "\n".join(lines)


def answer(query, top_k=TOP_K, history=None):
    """Retrieval & Context Injection -> Generation & Formatting. Returns the reply text
    and the retrieved chunks (so the caller/demo can show what was retrieved)."""
    chunks = retrieve(query, top_k=top_k)
    context = format_context(chunks)

    messages = [{"role": "system", "content": FRIDAY_SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({
        "role": "user",
        "content": f"CONTEXT:\n{context}\n\nQUESTION: {query}\n\nAnswer using ONLY the context above.",
    })

    reply = chat(messages)
    return reply, chunks
