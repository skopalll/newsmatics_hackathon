from config import LOG_FILE, DB_FILE
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

def create_topics_table():
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
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM topics")
    topics = cursor.fetchall()
    conn.close()
    return topics

def create_keywords_table():
    """Creates a sample users table if not exists"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS keywords (
                        id INTEGER PRIMARY KEY,
                        keywords TEXT NOT NULL,
                        FOREIGN KEY (id) REFERENCES topics(id))''')
    conn.commit()
    conn.close()
    log("Database table created successfully")

def add_keywords(id, keywords):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO keywords (id, keywords) VALUES (?, ?)", (id, keywords))
        conn.commit()
        conn.close()
        log(f"Added keywords for topic {id}: {keywords}")
    except sqlite3.IntegrityError:
        log(f"Failed to add keywords for topic {id}: Integrity error", "warning")

def update_keywords(id, keywords):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE keywords SET keywords = ?, WHERE id = ?", (keywords, id))
        conn.commit()
        conn.close()
        log(f"Added keywords for topic {id}: {keywords}")
    except sqlite3.IntegrityError:
        log(f"Failed to add keywords for topic {id}: Integrity error", "warning")

def delete_keywords(id):
    """Deletes keywords for a given topic by its id"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM keywords WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        log(f"Deleted keywords for topic {id}")
    except sqlite3.Error as e:
        log(f"Failed to delete keywords for topic {id}: {e}", "warning")

def get_keyword(id):
    """Fetches a keyword by its id from the database"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM keywords WHERE id = ?", (id,))
    one_keyword = cursor.fetchall()
    conn.close()
    return one_keyword

def get_keywords():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM keywords")
    returned_keywords = cursor.fetchall()
    conn.close()
    return returned_keywords


