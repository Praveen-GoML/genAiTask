"""
src/core/llm.py - wrapper around the Groq API for ultra-fast cloud LLM inference.
"""

import requests

from config.settings import settings

GROQ_API_KEY = settings.GROQ_API_KEY
GROQ_MODEL = settings.GROQ_MODEL
GROQ_BASE_URL = settings.GROQ_BASE_URL


class GroqUnavailable(RuntimeError):
    pass


# Backward compatibility alias
OllamaUnavailable = GroqUnavailable


def chat(messages, temperature=0.4, model=None):
    """messages: list of {"role": "system"|"user"|"assistant", "content": str}
    Returns the assistant's reply text via Groq's OpenAI-compatible API."""
    model = model or GROQ_MODEL
    url = f"{GROQ_BASE_URL.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
    except requests.exceptions.RequestException as e:
        raise GroqUnavailable(f"Could not connect to Groq API endpoint: {e}")

    if resp.status_code == 401:
        raise GroqUnavailable("Invalid Groq API key. Check GROQ_API_KEY in .env.")
    elif resp.status_code == 404:
        raise GroqUnavailable(f"Groq model '{model}' not found or unavailable.")
    
    try:
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        raise GroqUnavailable(f"Groq API call failed (HTTP {resp.status_code}): {resp.text}")


def groq_alive():
    """Health check verifying Groq API reachability and key validity."""
    if not GROQ_API_KEY:
        return False
    url = f"{GROQ_BASE_URL.rstrip('/')}/models"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        return r.status_code == 200
    except Exception:
        return False


FRIDAY_SYSTEM_PROMPT = getattr(settings, "FRIDAY_SYSTEM_PROMPT", "")


class FridayLLMEngine:
    def __init__(self, model_name: str = None, base_url: str = None):
        self.model_name = model_name or GROQ_MODEL

    def query(self, prompt: str, context: str = "", system_override: str = None) -> str:
        system_instruction = system_override if system_override else FRIDAY_SYSTEM_PROMPT
        messages = [{"role": "system", "content": system_instruction}]
        if context:
            messages.append({"role": "user", "content": f"Context: {context}\n\nUser: {prompt}"})
        else:
            messages.append({"role": "user", "content": prompt})

        try:
            return chat(messages, model=self.model_name)
        except Exception as e:
            return f"Boss, we have a connection issue with the LLM cluster: {str(e)}"


# Backward compatibility alias
ollama_alive = groq_alive

