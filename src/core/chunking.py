"""
src/core/chunking.py - different chunking strategies for different FitMind AI knowledge types.

Demonstrates the Ingestion & Chunking lesson across two axes:
  - Content STRUCTURE differs (a FAQ vs. a workout plan needs a different split)
  - File FORMAT differs (plain text, Markdown, JSON, CSV — each needs its own parser)

Each function returns a list of (text, metadata) chunks.
"""

import json
import os
import re

from config.settings import settings

DOCUMENTS_DIR = settings.DOCUMENTS_DIR


def _read(filename: str) -> str:
    path = os.path.join(DOCUMENTS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Chunking strategies
# ---------------------------------------------------------------------------

def chunk_by_paragraph(filename: str, doc_type: str) -> list:
    """Paragraph-level semantic chunking — for plain-text guides (nutrition, supplements,
    recovery, injury prevention, workout plans, goal setting).
    Each concept/protocol needs its full reasoning kept intact in one chunk."""
    text = _read(filename)
    paragraphs = [
        p.strip().replace("\n", " ")
        for p in re.split(r"\n\s*\n", text)
        if p.strip() and not p.strip().startswith("#")
    ]
    return [
        (p, {"doc_type": doc_type, "source": filename, "strategy": "paragraph"})
        for p in paragraphs
    ]


def chunk_by_markdown_header(filename: str, doc_type: str) -> list:
    """Markdown header-aware chunking — for FAQ and meal plans.
    Splits on '## ' section boundaries so each Q&A or meal plan section stays together."""
    text = _read(filename)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    sections = re.split(r"\n(?=## )", text.strip())
    chunks = []
    for section in sections:
        section = section.strip()
        if not section or section.startswith("# "):
            continue  # skip the lone H1 title
        title_match = re.match(r"##\s*(.+)", section)
        title = title_match.group(1).strip() if title_match else "Untitled section"
        flat = re.sub(r"\s+", " ", section).strip()
        chunks.append((
            flat,
            {"doc_type": doc_type, "source": filename, "strategy": "markdown_header", "title": title},
        ))
    return chunks


def chunk_by_json_record(filename: str, doc_type: str) -> list:
    """Structured JSON chunking — for exercise_library.json and member_profiles.json.
    One array element = one chunk, so every field is represented and none silently dropped.
    Uses json.load, never regex/text-splitting on raw JSON."""
    records = json.loads(_read(filename))
    chunks = []
    for record in records:
        # Use 'name' as the primary identifier for both exercises and member profiles
        name = record.get("name", record.get("id", "Unknown"))
        fields = "; ".join(
            f"{k.replace('_', ' ').capitalize()}: {v}"
            for k, v in record.items()
            if k not in ("name", "id")
        )
        flat = f"{name} — {fields}"
        chunks.append((
            flat,
            {"doc_type": doc_type, "source": filename, "strategy": "json_record", "name": name},
        ))
    return chunks


def chunk_by_section_header(filename: str, doc_type: str) -> list:
    """All-caps section header chunking — for structured text files that use
    ===== or ----- separator lines (supplement_guide.txt, injury_prevention.txt).
    Each named section becomes one chunk."""
    text = _read(filename)
    # Split on lines that are all dashes or equals (section dividers)
    blocks = re.split(r"\n[=\-]{4,}\n", text)
    chunks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        flat = re.sub(r"\s+", " ", block).strip()
        # Extract first non-empty line as the title
        first_line = next((l.strip() for l in block.splitlines() if l.strip()), "Section")
        chunks.append((
            flat,
            {"doc_type": doc_type, "source": filename, "strategy": "section_header", "title": first_line},
        ))
    return chunks


def chunk_by_workout_block(filename: str, doc_type: str) -> list:
    """Workout-block chunking — for workout_plans.txt.
    Splits on all-caps section headings (e.g. 'BEGINNER FULL-BODY PROGRAM') so each
    program stays together as one retrievable chunk."""
    text = _read(filename)
    # Split on lines that are all-caps headings (optional dashes below)
    blocks = re.split(r"\n(?=[A-Z][A-Z \/\-&()]{5,}\n[-]+)", text)
    if len(blocks) <= 1:
        # Fallback: split on double newlines if pattern didn't match
        blocks = [b.strip() for b in re.split(r"\n\s*\n\n", text) if b.strip()]
    chunks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        first_line = next((l.strip() for l in block.splitlines() if l.strip()), "Program")
        flat = re.sub(r"\s+", " ", block).strip()
        chunks.append((
            flat,
            {"doc_type": doc_type, "source": filename, "strategy": "workout_block", "title": first_line},
        ))
    return chunks


# ---------------------------------------------------------------------------
# Ingestion plan: file → strategy → doc_type
# ---------------------------------------------------------------------------

INGESTION_PLAN = [
    # Plain-text paragraph-based guides
    (chunk_by_paragraph,        "nutrition_guide.txt",      "nutrition_guide"),
    (chunk_by_paragraph,        "recovery_protocols.txt",   "recovery_protocols"),
    (chunk_by_paragraph,        "goal_setting_guide.txt",   "goal_setting_guide"),
    # Structured text with section headers
    (chunk_by_section_header,   "supplement_guide.txt",     "supplement_guide"),
    (chunk_by_section_header,   "injury_prevention.txt",    "injury_prevention"),
    # Workout plans — block-level split
    (chunk_by_workout_block,    "workout_plans.txt",        "workout_plans"),
    # Markdown header-split documents
    (chunk_by_markdown_header,  "faq.md",                   "faq"),
    (chunk_by_markdown_header,  "meal_plans.md",            "meal_plans"),
    # JSON record-per-item documents
    (chunk_by_json_record,      "exercise_library.json",    "exercise_library"),
    (chunk_by_json_record,      "member_profiles.json",     "member_profiles"),
]


def build_all_chunks() -> list:
    """Runs the full ingestion plan and returns every (text, metadata) chunk."""
    all_chunks = []
    for chunk_fn, filename, doc_type in INGESTION_PLAN:
        chunks = chunk_fn(filename, doc_type)
        all_chunks.extend(chunks)
        print(f"  {filename:<28} -> {chunk_fn.__name__:<26} -> {len(chunks)} chunks")
    return all_chunks
