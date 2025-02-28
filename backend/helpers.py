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
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL)''')
    conn.commit()
    conn.close()
    log("Database table created successfully")

def add_user(name, email):
    """Adds a new user to the database"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        conn.close()
        log(f"Added user: {name}, {email}")
    except sqlite3.IntegrityError:
        log(f"Failed to add user {name}: Email already exists", "warning")

def delete_user(user_id):
    """Deletes a user by ID"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    log(f"Deleted user with ID: {user_id}")

def update_user(user_id, name, email):
    """Updates user information"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
    conn.commit()
    conn.close()
    log(f"Updated user {user_id} to {name}, {email}")

def get_users():
    """Fetches all users from the database"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

