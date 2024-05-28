from peewee import CharField, AutoField, DateTimeField, ForeignKeyField, Model
import datetime
import logging
from db import chat
from db import db_instance

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

# Table Schema
class Message(Model):
    id = AutoField()
    role = CharField()
    content = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    chat_id = ForeignKeyField(chat.Chat, backref='chat')

    class Meta:
        database = db_instance  

# Table Object
class MessageObj():
    def __init__(self, message):
        self.id = message.id
        self.role = message.role
        self.content = message.content
        self.created_at = message.created_at
        self.chat_obj = chat.ChatObj(chat.get(message.chat_id))

# Database Operations
def create(role, content, chat):
    message = Message.create(role=role, content=content, chat_id=chat.id)
    return MessageObj(message)

def get(message_id):
    message = Message.get_or_none(Message.id == message_id)
    
    if message is None:
        return None
    
    return MessageObj(message)

def list():
    messages = Message.select()
    return [MessageObj(message) for message in messages]

def list_by_chat(chat):
    messages = Message.select().where(Message.chat_id == chat.id)
    return [MessageObj(message) for message in messages]

def delete():
    Message.delete().execute()

def delete_by_chat(chat):
    Message.delete().where(Message.chat_id == chat.id).execute()