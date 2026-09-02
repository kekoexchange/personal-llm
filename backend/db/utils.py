from pathlib import Path
from db.message import Message
from db.chat import Chat
from db import db_instance

# Database Operations
def setup():
    Path(db_instance.database).parent.mkdir(parents=True, exist_ok=True)
    db_instance.connect()
    db_instance.create_tables([Message, Chat])