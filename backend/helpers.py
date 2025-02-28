from backend.config import LOG_FILE, DB_FILE
import sqlite3
import logging

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log(message, level="info"):
    """Logs messages to log.txt"""
    levels = {
        "info": logging.info,
        "warning": logging.warning,
        "error": logging.error
    }
    if level in levels:
        levels[level](message)
    else:
        logging.info(message)
    

def connect_db():
    """Connects to the SQLite database and returns the connection object"""
    conn = sqlite3.connect(DB_FILE)
    return conn

def create_table():
    """Creates a sample users table if not exists"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS topics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        title TEXT NOT NULL,
                        text TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    log("Database table created successfully")

def add_topic(date, title, text):
    """Adds a new user to the database"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO topics (date, title, text) VALUES (?, ?, ?)", (date, title, text))
        conn.commit()
        conn.close()
        log(f"Added topic: {title} on {date}")
    except sqlite3.IntegrityError:
        log(f"Failed to add topic {title}: Integrity error", "warning")

def delete_topic(id):
    """Deletes a user by ID"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM topics WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    log(f"Deleted user with ID: {id}")

def update_topic(id, date, title, text):
    """Updates user information"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE topics SET date = ?, title = ?, text = ? WHERE id = ?", (date, title, text, id))
    conn.commit()
    conn.close()
    log(f"Updated topic {id}: {title} on {date}")

def get_topics():
    """Fetches all users from the database"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM topics")
    users = cursor.fetchall()
    conn.close()
    return users

