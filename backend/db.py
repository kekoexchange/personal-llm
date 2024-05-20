from peewee import Model, SqliteDatabase, CharField, AutoField
import constants

db = SqliteDatabase(constants.DB_FILE_NAME)

# Database Schema
class Message(Model):
    id = AutoField()
    role = CharField()
    content = CharField()

    class Meta:
        database = db

# Database Operationss
def setup():
    db.connect()
    db.create_tables([Message])

def insert_message(role, content):
    message = Message.create(role=role, content=content)

def get_messages():
    messages = Message.select()
    return [(message.role, message.content) for message in messages]

def get_message(message_id):
    message = Message.get_or_none(id=message_id)
    if message:
        return (message.role, message.content)
    return None

def delete_messages():
    Message.delete().execute()