from db.message import Message
from db.chat import Chat
from db import db_instance

# Database Operations
def setup():
    db_instance.connect()
    db_instance.create_tables([Message, Chat])

    # TODO: Temporary code to create a single "chat" object until the frontend is implemented
    if not Chat.select().exists():
        Chat.create(name="default")

# TODO: Temporary code to return the default chat object until the frontend is implemented
def get_default_chat():
    return Chat.get(Chat.name == "default")
    