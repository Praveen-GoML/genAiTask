"""
src/core/llm.py - thin wrapper around the Groq online inference API.
Requires GROQ_API_KEY in your .env file.  See https://console.groq.com for a free key.

The message format (system / user / assistant roles) is identical to the old Ollama
wrapper, so every caller in src/ that was already using chat() continues to work
without changes.
"""

from groq import Groq, APIConnectionError, AuthenticationError

from config.settings import settings

GROQ_MODEL = settings.GROQ_MODEL

_client: Groq | None = None


def _get_client() -> Groq:
    """Lazy-init a single Groq client for the process lifetime."""
    global _client
    if _client is None:
        _client = Groq(api_key=settings.GROQ_API_KEY)
    return _client


class GroqUnavailable(RuntimeError):
    pass


def chat(messages, temperature=0.4, model=None):
    """messages: list of {"role": "system"|"user"|"assistant", "content": str}
    Returns the assistant's reply text.
    Raises GroqUnavailable with a friendly message on connection / auth failure."""
    model = model or GROQ_MODEL
    try:
        response = _get_client().chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except AuthenticationError:
        raise GroqUnavailable(
            "Groq authentication failed.\n"
            "Check that GROQ_API_KEY is set correctly in your .env file.\n"
            "Get a free key at https://console.groq.com"
        )
    except APIConnectionError as e:
        raise GroqUnavailable(
            f"Could not reach the Groq API: {e}\n"
            "Check your internet connection and try again."
        )
    except Exception as e:
        raise GroqUnavailable(f"Groq call failed: {e}")


def groq_alive() -> bool:
    """Best-effort health check — tries a minimal completion. Used by the health endpoint."""
    try:
        _get_client().chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1,
            temperature=0.0,
        )
        return True
    except Exception:
        return False
