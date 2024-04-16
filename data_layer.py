import sqlite3

DATABASE_NAME = 'data.db'

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

def setup():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT
        )
    ''')
    return conn, cursor

# Function to insert a single message into the "messages" table
def insert_message(role, content):
    cursor.execute('INSERT INTO messages (role, content) VALUES (?, ?)', (role, content))
    conn.commit()

# Function to retrieve all messages from the "messages" table
def retrieve_all_messages():
    cursor.execute('SELECT role, content FROM messages')
    return cursor.fetchall()

# Function to retrieve a specific message from the "messages" table
def retrieve_message(message_id):
    cursor.execute('SELECT role, content FROM messages WHERE id = ?', (message_id,))
    return cursor.fetchone()

def clear_messages():
    cursor.execute('DELETE FROM messages')
    conn.commit()

# Close the database connection
def teardown():
    cursor.close()
    conn.close()