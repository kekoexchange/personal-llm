from peewee import CharField, AutoField, DateTimeField
from backend.db.message import Message, MessageObj
import datetime
import logging
from . import BaseModel 

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

# Table Schema
class Chat(BaseModel):
    id = AutoField()
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

# Table Object
class ChatObj():
    def __init__(self, chat):
        self.id = chat.id
        self.name = chat.name
        self.created_at = chat.created_at

    def get_messages(self):
        messages = Message.select().where(Message.chat_id == self.id)
        return [MessageObj(message) for message in messages]

# Database Operations
def create_chat(name):
    chat = Chat.create(name=name)
    return ChatObj(chat)

def get_chats():
    chats = Chat.select()
    return [ChatObj(chat) for chat in chats]

def delete_chats():
    Chat.delete().execute()

    