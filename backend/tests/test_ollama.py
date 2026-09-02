"""Tests that talk to the REAL Ollama server (localhost:11434, or $OLLAMA_HOST).

They are part of the normal backend run because the app cannot work without
Ollama. If Ollama is not running, cannot be reached, or the configured model
has not been pulled, these tests FAIL with a message that says what to do.
Every call has a deadline, so a server that accepts connections but never
answers fails the test instead of hanging it.

To run everything except these:  ./.venv/bin/python -m pytest -m "not ollama"
"""
import os
from types import SimpleNamespace

import ollama
import pytest

import constants
from llm import dispatch

pytestmark = pytest.mark.ollama

HOST = os.environ.get("OLLAMA_HOST", "localhost:11434")
LIST_TIMEOUT = 5  # seconds to wait for Ollama to answer "which models do you have?"
CHAT_TIMEOUT = 120  # seconds to wait for each streamed chunk of a reply

NOT_RUNNING = (
    f"Could not talk to Ollama at {HOST}. "
    "Start it with `npm run setup` (or `ollama serve`) and rerun the tests."
)


def one_line(error):
    """e.g. 'ConnectError: [Errno 111] Connection refused' - first line only."""
    text = str(error).strip().splitlines()[0] if str(error).strip() else ""
    if hasattr(error, "status_code"):  # ollama.ResponseError: what the server said
        text = f"HTTP {error.status_code} {text}".strip()
    return f"{type(error).__name__}: {text or '(no details)'}"


def wanted_model():
    # Ollama lists untagged names as "<name>:latest"
    name = constants.LLM_MODEL
    return name if ":" in name else f"{name}:latest"


def installed_models():
    """Model names Ollama has downloaded, or a clear FAIL if it cannot be reached."""
    try:
        listed = ollama.Client(timeout=LIST_TIMEOUT).list()
    except Exception as error:  # refused, timed out, not an Ollama server, ...
        problem = one_line(error)
        listed = None
    if listed is None:  # outside the except: so the report shows only our message
        pytest.fail(f"{NOT_RUNNING}\n(underlying error: {problem})", pytrace=False)
    return [m.model for m in listed.models]


def require_model():
    models = installed_models()
    assert wanted_model() in models, (
        f"Model {constants.LLM_MODEL!r} is not downloaded in Ollama (found: {models}). "
        f"Run `ollama pull {constants.LLM_MODEL}` (`npm run start` does this automatically)."
    )


def test_ollama_server_is_running():
    installed_models()


def test_configured_model_is_downloaded():
    require_model()


def test_real_streamed_chat_returns_text(monkeypatch):
    require_model()
    # dispatch calls the module-level ollama.chat, which waits forever. Swap in
    # the same function from a client with a deadline so a wedged server fails
    # this test instead of hanging it. Everything else about the call is real.
    monkeypatch.setattr(ollama, "chat", ollama.Client(timeout=CHAT_TIMEOUT).chat)
    prompt = [SimpleNamespace(role="user", content="Reply with the single word: hello")]

    try:
        reply = "".join(chunk["message"]["content"] for chunk in dispatch.send_message(prompt))
    except Exception as error:
        problem = one_line(error)
        reply = None
    if reply is None:
        pytest.fail(
            f"Ollama at {HOST} did not complete a chat with {constants.LLM_MODEL!r} "
            f"within {CHAT_TIMEOUT}s per chunk.\n(underlying error: {problem})\n"
            "Check the server: `ollama ps`, or its log (storage/ollama.log when started by npm run setup).",
            pytrace=False,
        )

    assert reply.strip() != "", f"{constants.LLM_MODEL} streamed back no text"
