"""
src/ui/streamlit_app.py - Streamlit chat interface for the JARVIS demo.

Run from the project root (with the API already running - see README):
    streamlit run src/ui/streamlit_app.py

This is a THIN HTTP CLIENT of src/api - it has no RAG/Agentic/NL2SQL logic of its own,
same as src/ui/cli.py. Lets you switch between RAG mode (JARVIS replies, grounded in his
knowledge base) and Agentic mode (JARVIS can also call tools - including the structured
fleet database via NL2SQL - and take simulated actions), and shows exactly what's
happening under the hood: retrieved sources in RAG mode, the full
Thought/Action/Observation trace (including any generated SQL) in Agentic mode.
"""

import os
import sys
import uuid

import requests
import streamlit as st

# Allow running via `streamlit run src/ui/streamlit_app.py` from the project root:
# Streamlit puts this script's own directory (src/ui) on sys.path, not the project
# root, so the top-level `config` package wouldn't otherwise be importable.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.settings import settings

API_BASE_URL = settings.API_BASE_URL

st.set_page_config(page_title="J.A.R.V.I.S.", page_icon="\U0001F916", layout="centered")


# ---------- session state ----------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "mode" not in st.session_state:
    st.session_state.mode = "RAG"
if "history" not in st.session_state:
    st.session_state.history = {"RAG": [], "Agentic": []}  # list of {"role", "content", "meta"/"trace"}


def reset_conversation():
    mode_key = "rag" if st.session_state.mode == "RAG" else "agent"
    try:
        requests.delete(f"{API_BASE_URL}/api/v1/chat/session/{st.session_state.session_id}",
                         params={"mode": mode_key}, timeout=5)
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


# ---------- sidebar ----------
with st.sidebar:
    st.title("J.A.R.V.I.S.")
    st.caption("RAG & Agentic AI demo - built entirely with open-source tools.")

    mode = st.radio("Mode", ["RAG", "Agentic"], index=0 if st.session_state.mode == "RAG" else 1,
                     help="RAG only replies, grounded in the knowledge base. Agentic can also call "
                          "tools - including querying the structured fleet database - and take simulated actions.")
    if mode != st.session_state.mode:
        st.session_state.mode = mode

    st.divider()
    st.subheader("System status")

    health = get_health()
    api_ok = health is not None
    st.write(("✅" if api_ok else "⚠️") + " API " + ("reachable" if api_ok else "not reachable"))
    if not api_ok:
        st.caption(f"Could not reach {API_BASE_URL} - is `uvicorn src.api.main:app` running?")

    kb_ok = bool(health and health.get("knowledge_base"))
    st.write(("✅" if kb_ok else "⚠️") + " Knowledge base " + ("ready" if kb_ok else "not built yet"))
    if api_ok and not kb_ok:
        st.caption("Run `python -m scripts.ingest` from the project root, then reload this page.")

    ollama_ok = bool(health and health.get("ollama"))
    st.write(("✅" if ollama_ok else "⚠️") + " Ollama " + ("reachable" if ollama_ok else "not reachable"))
    if api_ok and not ollama_ok:
        st.caption("Install Ollama, pull a model, and make sure it's running - see README.")

    postgres_ok = bool(health and health.get("postgres"))
    st.write(("✅" if postgres_ok else "⚠️") + " Fleet DB " + ("reachable" if postgres_ok else "not reachable"))
    if api_ok and not postgres_ok:
        st.caption("Run `docker compose up -d postgres`, then `python -m scripts.setup_db` and `python -m scripts.seed_db`.")

    st.divider()
    if st.button("Clear conversation", use_container_width=True):
        reset_conversation()
        st.rerun()

    st.divider()
    st.caption("Every RAG/Agentic/NL2SQL component taught in the course is implemented in "
               "`src/` behind the FastAPI service in `src/api/` - see the README's mapping table.")


# ---------- main chat area ----------
st.header(f"Chat with JARVIS — {st.session_state.mode} mode")
if st.session_state.mode == "RAG":
    st.caption("JARVIS answers only from his knowledge base. He never takes an action.")
else:
    st.caption("JARVIS can call tools (including the structured fleet database) and take "
               "simulated actions - watch the reasoning trace under each reply.")


def render_trace(trace):
    with st.expander("See JARVIS's reasoning (Thought → Action → Observation)"):
        for i, step in enumerate(trace, 1):
            st.markdown(f"**Step {i} - Thought:** {step['thought']}")
            if step["action"] and step["action"].lower() != "none":
                st.markdown(f"**Action:** `{step['action']}({step['action_input']})`")
            if step.get("observation"):
                st.markdown(f"**Observation:** {step['observation']}")
            if i < len(trace):
                st.markdown("---")


for msg in st.session_state.history[st.session_state.mode]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("meta"):
            st.caption(msg["meta"])
        if msg.get("trace"):
            render_trace(msg["trace"])

query = st.chat_input("Ask JARVIS something...")

if query:
    st.session_state.history[st.session_state.mode].append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        if not api_ok:
            st.error(f"Can't reach the API at {API_BASE_URL} - make sure `uvicorn src.api.main:app` is running.")
        elif not kb_ok:
            st.warning("The knowledge base hasn't been built yet - run `python -m scripts.ingest` first.")
        elif not ollama_ok:
            st.warning("Can't reach Ollama - make sure it's installed, running, and a model is pulled.")
        else:
            with st.spinner("JARVIS is thinking..."):
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
                    st.error(f"Request to JARVIS's API failed: {e}")
                    data = None

                if data:
                    reply = data["reply"]
                    st.markdown(reply)
                    if st.session_state.mode == "RAG":
                        meta = "Retrieved from: " + ", ".join(data["citations"]) if data.get("citations") else None
                        if meta:
                            st.caption(meta)
                        st.session_state.history["RAG"].append({"role": "assistant", "content": reply, "meta": meta})
                    else:
                        trace = data.get("trace") or []
                        render_trace(trace)
                        st.session_state.history["Agentic"].append({"role": "assistant", "content": reply, "trace": trace})
