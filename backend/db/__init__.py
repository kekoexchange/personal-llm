from peewee import SqliteDatabase
import constants

db_instance = SqliteDatabase(constants.DB_FILE_NAME, pragmas={'foreign_keys': 1})