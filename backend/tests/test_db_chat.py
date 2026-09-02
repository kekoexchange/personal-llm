"""db/chat.py: create / get / list / delete against a temporary database."""
import datetime

from db import chat


def test_create_returns_chat_with_id_and_name():
    created = chat.create("My first chat")

    assert created.id is not None
    assert created.name == "My first chat"
    assert isinstance(created.created_at, datetime.datetime)


def test_get_returns_the_saved_chat():
    created = chat.create("Find me")

    found = chat.get(created.id)

    assert found.id == created.id
    assert found.name == "Find me"


def test_get_returns_none_for_unknown_id():
    assert chat.get(9999) is None


def test_list_returns_chats_in_creation_order():
    chat.create("first")
    chat.create("second")

    names = [c.name for c in chat.list()]

    assert names == ["first", "second"]


def test_list_is_empty_on_a_fresh_database():
    assert chat.list() == []


def test_delete_removes_the_chat():
    keep = chat.create("keep")
    gone = chat.create("gone")

    chat.delete(gone.id)

    assert chat.get(gone.id) is None
    assert [c.id for c in chat.list()] == [keep.id]


def test_to_front_end_shape():
    created = chat.create("shape")

    data = created.toFrontEnd()

    assert set(data) == {"id", "name", "created_at"}
    assert data["id"] == created.id
    assert data["name"] == "shape"
    # created_at is sent to the browser as an ISO-8601 string
    assert datetime.datetime.fromisoformat(data["created_at"]) == created.created_at
