from peewee import CharField, AutoField, DateTimeField, Model
import logging
import datetime
from db import db_instance

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

# Table Schema
class Chat(Model):
    id = AutoField()
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db_instance

# Table Object
class ChatObj():
    def __init__(self, chat):
        
        self.id = chat.id
        self.name = chat.name
        self.created_at = chat.created_at
    
    def toFrontEnd(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }

# Database Operations
def create(name):
    chat = Chat.create(name=name)
    return ChatObj(chat)

def get(chat_id):
    chat = Chat.get_or_none(Chat.id == chat_id)

    if chat is None:
        return None
    
    return ChatObj(chat)

def list():
    chats = Chat.select()
    return [ChatObj(chat) for chat in chats]

def delete(chat_id):
    Chat.delete().where(Chat.id == chat_id).execute()

    