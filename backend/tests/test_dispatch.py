"""llm/dispatch.py builds the prompt for Ollama. ollama.chat is replaced by a
fake here, so these tests need no Ollama server (see test_ollama.py for the
real thing)."""
from types import SimpleNamespace

import ollama
import pytest

import constants
from llm import dispatch


@pytest.fixture
def ollama_calls(monkeypatch):
    """Replace ollama.chat with a fake that records how it was called."""
    calls = []

    def fake_chat(**kwargs):
        calls.append(kwargs)
        return iter([])  # an empty stream

    monkeypatch.setattr(ollama, "chat", fake_chat)
    return calls


def a_message(role, content):
    # dispatch only reads .role and .content, like db.message.MessageObj has
    return SimpleNamespace(role=role, content=content)


def test_system_prompt_comes_first(ollama_calls):
    dispatch.send_message([a_message("user", "hi")])

    first = ollama_calls[0]["messages"][0]
    assert first == {"role": "system", "content": constants.LLM_SYSTEM_PROMPT}


def test_history_follows_with_roles_and_content_preserved(ollama_calls):
    history = [
        a_message("user", "What is 2+2?"),
        a_message("assistant", "4"),
        a_message("user", "And 3+3?"),
    ]

    dispatch.send_message(history)

    sent = ollama_calls[0]["messages"][1:]  # everything after the system prompt
    assert sent == [
        {"role": "user", "content": "What is 2+2?"},
        {"role": "assistant", "content": "4"},
        {"role": "user", "content": "And 3+3?"},
    ]


def test_uses_the_configured_model_and_streams(ollama_calls, monkeypatch):
    # a value that is NOT the default, so a hard-coded model name would fail here
    monkeypatch.setattr(constants, "LLM_MODEL", "some-other-model:1b")

    dispatch.send_message([a_message("user", "hi")])

    assert ollama_calls[0]["model"] == "some-other-model:1b"
    assert ollama_calls[0]["stream"] is True


def test_returns_the_stream_from_ollama(monkeypatch):
    chunks = [{"message": {"content": "Hel"}}, {"message": {"content": "lo"}}]
    monkeypatch.setattr(ollama, "chat", lambda **kwargs: iter(chunks))

    stream = dispatch.send_message([a_message("user", "hi")])

    assert list(stream) == chunks
