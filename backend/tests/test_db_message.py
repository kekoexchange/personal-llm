"""db/message.py: messages belong to a chat; CRUD against a temporary database."""
import datetime

import peewee
import pytest

from db import chat, message


@pytest.fixture
def a_chat():
    return chat.create("chat under test")


def test_create_returns_message_with_role_content_and_chat(a_chat):
    created = message.create("user", "hello", a_chat.id)

    assert created.id is not None
    assert created.role == "user"
    assert created.content == "hello"
    assert created.chat_obj.id == a_chat.id
    assert isinstance(created.created_at, datetime.datetime)


def test_create_rejects_a_chat_that_does_not_exist():
    # foreign keys are switched on for the SQLite connection
    with pytest.raises(peewee.IntegrityError):
        message.create("user", "orphan", 9999)


def test_get_returns_the_saved_message(a_chat):
    created = message.create("assistant", "hi there", a_chat.id)

    found = message.get(created.id)

    assert found.id == created.id
    assert found.role == "assistant"
    assert found.content == "hi there"


def test_get_returns_none_for_unknown_id():
    assert message.get(9999) is None


def test_list_by_chat_only_returns_that_chats_messages_in_order(a_chat):
    other = chat.create("other chat")
    message.create("user", "one", a_chat.id)
    message.create("assistant", "two", a_chat.id)
    message.create("user", "not mine", other.id)

    mine = message.list_by_chat(a_chat.id)

    assert [(m.role, m.content) for m in mine] == [("user", "one"), ("assistant", "two")]


def test_list_returns_every_message(a_chat):
    other = chat.create("other chat")
    message.create("user", "one", a_chat.id)
    message.create("user", "two", other.id)

    assert [m.content for m in message.list()] == ["one", "two"]


def test_delete_by_chat_leaves_other_chats_alone(a_chat):
    other = chat.create("other chat")
    message.create("user", "mine", a_chat.id)
    message.create("user", "theirs", other.id)

    message.delete_by_chat(a_chat.id)

    assert message.list_by_chat(a_chat.id) == []
    assert [m.content for m in message.list_by_chat(other.id)] == ["theirs"]


def test_delete_removes_all_messages(a_chat):
    message.create("user", "one", a_chat.id)
    message.create("user", "two", a_chat.id)

    message.delete()

    assert message.list() == []


def test_to_front_end_shape_includes_the_chat(a_chat):
    created = message.create("user", "shape", a_chat.id)

    data = created.toFrontEnd()

    assert set(data) == {"id", "role", "content", "created_at", "chat"}
    assert data["role"] == "user"
    assert data["content"] == "shape"
    assert datetime.datetime.fromisoformat(data["created_at"]) == created.created_at
    assert data["chat"] == a_chat.toFrontEnd()
