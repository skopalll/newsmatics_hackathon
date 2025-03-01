from config import LOG_FILE, DB_FILE
import sqlite3
import logging


# CLOSE YOUR EYES

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
                        keywords TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    log("Database table created successfully")

def add_topic(date, title, keywords) -> int:
    """Adds a new user to the database"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO topics (date, title, keywords) VALUES (?, ?, ?)", (date, title, keywords))
        last_id = cursor.lastrowid
        conn.commit()
        conn.close()
        log(f"Added topic: {title} on {date} with {keywords}")
        return last_id
    except sqlite3.IntegrityError:
        log(f"Failed to add topic {title}: Integrity error", "error")

def delete_topic(id):
    """Deletes a user by ID"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM topics WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    log(f"Deleted topic with ID: {id}")

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

def get_topics_by_date(date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM topics WHERE date = ?", (date,))
    topics = cursor.fetchall()
    conn.close()
    return topics

def pls_delete_all_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        if table_name != 'sqlite_sequence':  # Avoid dropping the sequence table that stores AUTOINCREMENT info
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            log(f"Dropped table: {table_name}")

    conn.commit()
    conn.close()  # Close the connection after all tables are dropped
    log("All tables have been deleted.")

def create_articles_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles (
                                article_id TEXT NOT NULL,
                                topic_id INTEGER,
                                title TEXT NOT NULL,
                                time TEXT NOT NULL,
                                politics TEXT NOT NULL,
                                credibility TEXT NOT NULL,
                                latitude REAL,
                                longitude REAL,
                                url TEXT NOT NULL,
                                FOREIGN KEY (topic_id) REFERENCES topics(id))''')
    conn.commit()
    conn.close()
    log("Database table created successfully")

def add_article(article_id, topic_id, title, time, coords, politics, credibility, url):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        lat, long = coords

        # Correct number of placeholders in the INSERT statement
        cursor.execute('''INSERT INTO articles (article_id, topic_id, title, time, politics, credibility, latitude, longitude, url)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (article_id, topic_id, title, time, politics, credibility, lat, long, url))

        conn.commit()
        log(f"Added article with topic ID: {topic_id}")
        conn.close()

    except sqlite3.Error as e:
        log(f"Failed to add article: {article_id, topic_id}", "error")

def delete_article(article_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles WHERE article_id = ?", (article_id,))
    conn.commit()
    conn.close()
    log(f"Deleted article with ID: {article_id}")

def get_articles_by_topic_id(topic_id):
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT article_id, title, time, latitude, longitude, politics, credibility, url
            FROM articles
            WHERE topic_id = ?
            ORDER BY time ASC
        ''', (topic_id,))
        articles = cursor.fetchall()
        return articles
    except sqlite3.Error as e:
        log(f"Failed to get articles for topic_id {topic_id}: {e}", "error")
        return []
    finally:
        if conn:
            conn.close()


def clear_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM topics")
    cursor.execute("DELETE FROM articles")
    conn.commit()
    conn.close()
    create_articles_table()
    create_topics_table()

