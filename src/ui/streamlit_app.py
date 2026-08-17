"""
src/ui/streamlit_app.py - Streamlit chat interface for FitMind AI.

Run from the project root (with the API already running):
    streamlit run src/ui/streamlit_app.py

This is a THIN HTTP CLIENT of src/api — it has no RAG/Agentic/NL2SQL logic of its own.
Switch between RAG mode (answers grounded in the knowledge base) and Agentic mode
(FitMind AI can also call tools — including the fitness database via NL2SQL — and take
simulated actions like logging a workout or setting a goal).
"""

import os
import sys
import uuid

import requests
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.settings import settings

API_BASE_URL = settings.API_BASE_URL

st.set_page_config(
    page_title="FitMind AI",
    page_icon="💪",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Session state init
# ---------------------------------------------------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "mode" not in st.session_state:
    st.session_state.mode = "RAG"
if "history" not in st.session_state:
    st.session_state.history = {"RAG": [], "Agentic": []}


def reset_conversation():
    mode_key = "rag" if st.session_state.mode == "RAG" else "agent"
    try:
        requests.delete(
            f"{API_BASE_URL}/api/v1/chat/session/{st.session_state.session_id}",
            params={"mode": mode_key},
            timeout=5,
        )
    except requests.exceptions.RequestException:
        pass
    st.session_state.history[st.session_state.mode] = []


def get_health():
    try:
        r = requests.get(f"{API_BASE_URL}/health", timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException:
        return None


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("💪 FitMind AI")
    st.caption("Your AI-powered personal fitness & nutrition coach.")

    mode = st.radio(
        "Mode",
        ["RAG", "Agentic"],
        index=0 if st.session_state.mode == "RAG" else 1,
        help=(
            "RAG: answers grounded strictly in the knowledge base (nutrition guides, "
            "workout plans, supplements, etc.).\n\n"
            "Agentic: can also call tools — query the fitness database, calculate macros, "
            "log workouts, set goals — and shows its full reasoning trace."
        ),
    )
    if mode != st.session_state.mode:
        st.session_state.mode = mode

    st.divider()
    st.subheader("System status")

    health = get_health()
    api_ok = health is not None

    st.write(("✅" if api_ok else "⚠️") + " API " + ("reachable" if api_ok else "not reachable"))
    if not api_ok:
        st.caption(f"Could not reach {API_BASE_URL} — is `uvicorn src.api.main:app` running?")

    kb_ok = bool(health and health.get("knowledge_base"))
    st.write(("✅" if kb_ok else "⚠️") + " Knowledge base " + ("ready" if kb_ok else "not built yet"))
    if api_ok and not kb_ok:
        st.caption("Run `python -m scripts.ingest` from the project root, then reload this page.")

    groq_ok = bool(health and health.get("groq"))
    st.write(("✅" if groq_ok else "⚠️") + " Groq LLM " + ("reachable" if groq_ok else "not reachable"))
    if api_ok and not groq_ok:
        st.caption(
            "Check that GROQ_API_KEY is set correctly in your .env file. "
            "Get a free key at https://console.groq.com"
        )

    postgres_ok = bool(health and health.get("postgres"))
    st.write(("✅" if postgres_ok else "⚠️") + " Fitness DB " + ("reachable" if postgres_ok else "not reachable"))
    if api_ok and not postgres_ok:
        st.caption(
            "Run `docker compose up -d postgres`, then "
            "`python -m scripts.setup_db` and `python -m scripts.seed_db`."
        )

    st.divider()

    if st.button("Clear conversation", use_container_width=True):
        reset_conversation()
        st.rerun()

    st.divider()
    st.caption(
        "FitMind AI combines RAG, Agentic AI, NL2SQL, and long-term memory to deliver "
        "personalised fitness and nutrition coaching. All components live in `src/`."
    )

    st.divider()
    st.markdown("**Try asking:**")
    if st.session_state.mode == "RAG":
        st.markdown(
            "- *What should I eat before a workout?*\n"
            "- *What are the cues for a good deadlift?*\n"
            "- *Is creatine safe to take daily?*\n"
            "- *How do I prevent shin splints?*\n"
            "- *Give me a fat-loss meal plan.*"
        )
    else:
        st.markdown(
            "- *Calculate my macros for 80 kg, muscle gain, moderately active.*\n"
            "- *What's my BMI at 82 kg and 178 cm?*\n"
            "- *Log 4 sets of squats, 8 reps, 100 kg.*\n"
            "- *How many workout sessions did Alex do this week?*\n"
            "- *Set a goal: run 5K in under 25 minutes by December.*"
        )


# ---------------------------------------------------------------------------
# Main chat area
# ---------------------------------------------------------------------------
st.header(f"Chat with FitMind AI — {st.session_state.mode} mode")

if st.session_state.mode == "RAG":
    st.caption(
        "Answers grounded in the fitness & nutrition knowledge base. "
        "Sources shown under each reply."
    )
else:
    st.caption(
        "Can call tools (fitness database, macro calculator, workout logger) and take "
        "simulated actions — the full reasoning trace appears under each reply."
    )


def render_trace(trace: list):
    with st.expander("See FitMind AI's reasoning (Thought → Action → Observation)"):
        for i, step in enumerate(trace, 1):
            st.markdown(f"**Step {i} — Thought:** {step['thought']}")
            if step.get("action") and step["action"].lower() != "none":
                st.markdown(f"**Action:** `{step['action']}({step['action_input']})`")
            if step.get("observation"):
                st.markdown(f"**Observation:** {step['observation']}")
            if i < len(trace):
                st.markdown("---")


# Render existing chat history
for msg in st.session_state.history[st.session_state.mode]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("meta"):
            st.caption(msg["meta"])
        if msg.get("trace"):
            render_trace(msg["trace"])

# Chat input
query = st.chat_input("Ask FitMind AI anything about fitness or nutrition...")

if query:
    st.session_state.history[st.session_state.mode].append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        if not api_ok:
            st.error(
                f"Can't reach the API at {API_BASE_URL} — "
                "make sure `uvicorn src.api.main:app` is running."
            )
        elif not kb_ok:
            st.warning(
                "The knowledge base hasn't been built yet — "
                "run `python -m scripts.ingest` first."
            )
        elif not groq_ok:
            st.warning(
                "Can't reach Groq — check your GROQ_API_KEY in .env and your internet connection."
            )
        else:
            with st.spinner("FitMind AI is thinking..."):
                endpoint = "rag" if st.session_state.mode == "RAG" else "agent"
                try:
                    resp = requests.post(
                        f"{API_BASE_URL}/api/v1/chat/{endpoint}",
                        json={"session_id": st.session_state.session_id, "query": query},
                        timeout=120,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                except requests.exceptions.RequestException as e:
                    st.error(f"Request to FitMind AI's API failed: {e}")
                    data = None

                if data:
                    reply = data["reply"]
                    st.markdown(reply)

                    if st.session_state.mode == "RAG":
                        meta = (
                            "Sources: " + ", ".join(data["citations"])
                            if data.get("citations")
                            else None
                        )
                        if meta:
                            st.caption(meta)
                        st.session_state.history["RAG"].append(
                            {"role": "assistant", "content": reply, "meta": meta}
                        )
                    else:
                        trace = data.get("trace") or []
                        if trace:
                            render_trace(trace)
                        st.session_state.history["Agentic"].append(
                            {"role": "assistant", "content": reply, "trace": trace}
                        )
