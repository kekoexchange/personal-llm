"""api/functions.py: the functions the browser calls through Python-Eel.

ollama.chat is stubbed, and js_update_current_message (the backend -> browser
push) is captured in a list, so these run without Ollama or a browser.
"""
import ollama
import pytest

from api import functions
from db import chat, message


@pytest.fixture
def pushed_to_browser(monkeypatch):
    """Collect every chunk py_send_message would have sent to the browser."""
    chunks = []
    monkeypatch.setattr(functions, "js_update_current_message", chunks.append)
    return chunks


@pytest.fixture
def ollama_says(monkeypatch):
    """Make ollama.chat stream the given pieces of text, recording the call."""
    calls = []

    def _install(*pieces):
        def fake_chat(**kwargs):
            calls.append(kwargs)
            return iter({"message": {"content": piece}} for piece in pieces)

        monkeypatch.setattr(ollama, "chat", fake_chat)
        return calls

    return _install


def test_send_message_streams_chunks_in_order_and_saves_both_rows(pushed_to_browser, ollama_says):
    ollama_says("Hel", "lo", "!")
    current = chat.create("chat")

    functions.py_send_message("Hi there", current.id)

    assert pushed_to_browser == ["Hel", "lo", "!"]
    saved = [(m.role, m.content) for m in message.list_by_chat(current.id)]
    assert saved == [("user", "Hi there"), ("assistant", "Hello!")]


def test_send_message_sends_the_whole_history_to_ollama(pushed_to_browser, ollama_says):
    calls = ollama_says("ok")
    current = chat.create("chat")
    message.create("user", "earlier question", current.id)
    message.create("assistant", "earlier answer", current.id)

    functions.py_send_message("follow-up", current.id)

    sent = calls[0]["messages"]
    assert sent[0]["role"] == "system"
    assert [(m["role"], m["content"]) for m in sent[1:]] == [
        ("user", "earlier question"),
        ("assistant", "earlier answer"),
        ("user", "follow-up"),
    ]


def test_send_message_reports_llm_errors_and_saves_no_assistant_row(pushed_to_browser, monkeypatch):
    def broken_chat(**kwargs):
        raise RuntimeError("model 'nope' not found")

    monkeypatch.setattr(ollama, "chat", broken_chat)
    current = chat.create("chat")

    functions.py_send_message("Hi", current.id)

    assert pushed_to_browser == ["[error] model 'nope' not found"]
    saved = [(m.role, m.content) for m in message.list_by_chat(current.id)]
    assert saved == [("user", "Hi")]  # the user's message is kept, nothing else


def test_create_chat_returns_front_end_dict():
    data = functions.py_create_chat("New chat")

    assert data["name"] == "New chat"
    assert chat.get(data["id"]).name == "New chat"


def test_get_chats_lists_every_chat():
    chat.create("a")
    chat.create("b")

    assert [c["name"] for c in functions.py_get_chats()] == ["a", "b"]


def test_get_messages_by_chat_returns_that_chats_messages():
    current = chat.create("chat")
    other = chat.create("other")
    message.create("user", "mine", current.id)
    message.create("user", "not mine", other.id)

    result = functions.py_get_messages_by_chat(current.id)

    assert [(m["role"], m["content"]) for m in result] == [("user", "mine")]


def test_delete_chat_removes_chat_and_its_messages():
    current = chat.create("chat")
    message.create("user", "bye", current.id)

    functions.py_delete_chat(current.id)

    assert chat.get(current.id) is None
    assert message.list_by_chat(current.id) == []
