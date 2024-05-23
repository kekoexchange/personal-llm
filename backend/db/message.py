from peewee import CharField, AutoField, ForeignKeyField, DateTimeField
from backend.db.chat import Chat, ChatObj
from . import BaseModel 
import datetime
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

# Table Schema
class Message(BaseModel):
    id = AutoField()
    role = CharField()
    content = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    chat_id = ForeignKeyField(Chat, backref='chat')

# Table Object
class MessageObj():
    def __init__(self, message):
        self.role = message.role
        self.content = message.content
        self.created_at = message.created_at
        self.chat_obj = ChatObj(message.chat)

# Database Operations
def create_message(role, content, chat):
    message = Message.create(role=role, content=content, chat=chat)
    return MessageObj(message)

def get_messages():
    messages = Message.select()
    return [MessageObj(message) for message in messages]

def delete_messages():
    Message.delete().execute()