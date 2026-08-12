"""
src/core/llm.py - thin wrapper around a local Ollama server. Open-source, runs entirely on
your own machine. See README for installing Ollama and pulling a model.
"""

import requests

from config.settings import settings

OLLAMA_HOST = settings.OLLAMA_HOST
OLLAMA_MODEL = settings.OLLAMA_MODEL


class OllamaUnavailable(RuntimeError):
    pass


def chat(messages, temperature=0.4, model=None):
    """messages: list of {"role": "system"|"user"|"assistant", "content": str}
    Returns the assistant's reply text. Raises OllamaUnavailable with a friendly
    message if Ollama isn't running or the model isn't pulled."""
    model = model or OLLAMA_MODEL
    try:
        resp = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json={"model": model, "messages": messages, "stream": False, "options": {"temperature": temperature}},
            timeout=120,
        )
    except requests.exceptions.ConnectionError:
        raise OllamaUnavailable(
            "Could not reach Ollama at " + OLLAMA_HOST + ".\n"
            "Is Ollama installed and running? See README.md 'Setup' section.\n"
            "Quick check: run `ollama list` in a terminal - if that fails, start Ollama first."
        )

    if resp.status_code == 404:
        raise OllamaUnavailable(
            f"Ollama is running, but the model '{model}' isn't pulled yet.\n"
            f"Run: ollama pull {model}"
        )
    resp.raise_for_status()
    data = resp.json()
    return data["message"]["content"]


def ollama_alive():
    """Best-effort health check used by the Streamlit sidebar."""
    try:
        r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False
