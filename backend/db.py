import sqlite3
import constants

conn = None
cursor = None

def setup():
    global conn, cursor
    conn = sqlite3.connect(constants.DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT
        )
    ''')

def insert_message(role, content):
    cursor.execute('INSERT INTO messages (role, content) VALUES (?, ?)', (role, content))
    conn.commit()

def get_messages():
    cursor.execute('SELECT role, content FROM messages')
    return cursor.fetchall()

def get_message(message_id):
    cursor.execute('SELECT role, content FROM messages WHERE id = ?', (message_id,))
    return cursor.fetchone()

def delete_messages():
    cursor.execute('DELETE FROM messages')
    conn.commit()

def teardown():
    cursor.close()
    conn.close()