from peewee import SqliteDatabase, Model
from backend.db.message import Message
from backend.db.chat import Chat
import constants

db = SqliteDatabase(constants.DB_FILE_NAME, pragmas={'foreign_keys': 1})

class BaseModel(Model):
    class Meta:
        database = db   

# Database Operations
def setup():
    db.connect()
    db.create_tables([Message, Chat])