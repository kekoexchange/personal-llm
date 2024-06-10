from db.message import Message
from db.chat import Chat
from db import db_instance

# Database Operations
def setup():
    db_instance.connect()
    db_instance.create_tables([Message, Chat])