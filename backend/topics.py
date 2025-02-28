import requests
import sqlite3
import datetime
from datetime import timedelta
from rake_nltk import Rake
import nltk

# Download NLTK stopwords if not already present
nltk.download('stopwords', quiet=True)

# Replace with your actual News API key
NEWS_API_KEY = '6e2b2763e36547f187b7a6669d0ddd27'

def fetch_news_for_date(date_str):
    """
    Fetches news articles for a specific date from News API.
    Uses the 'everything' endpoint with date filters.
    Returns aggregated text of titles and descriptions.
    """
    url = 'https://newsapi.org/v2/everything'
    params = {
        'from': date_str,
        'to': date_str,
        'language': 'en',
        'sortBy': 'popularity',
        'apiKey': NEWS_API_KEY,
        'pageSize': 100  # maximum articles per request
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except Exception as e:
        print("Error:", response.status_code, response.text)
        print(f"Error fetching news for {date_str}: {e}")
        return ""
    
    data = response.json()
    articles = data.get('articles', [])
    
    # Aggregate titles and descriptions into one text blob
    aggregated_text = " ".join(
        f"{article.get('title', '')} {article.get('description', '')}"
        for article in articles
    )
    return aggregated_text

def extract_keywords_rake(text):
    """
    Uses RAKE algorithm to extract keywords from the text.
    Returns a list of keywords sorted by their score.
    """
    if not text.strip():
        return []
    
    r = Rake()  # Uses default stopwords from NLTK
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases()  # Keywords are sorted by score (highest first)
    return keywords

def get_top_three_keywords(keywords):
    """
    Returns the top three keywords from the list.
    """
    if not keywords:
        return []
    return keywords[:3]

def save_topics_to_db(date_str, topics):
    """
    Saves the topics for the given date in the SQLite database.
    The table 'daily_topics' has columns: date, topic1, topic2, topic3.
    """
    conn = sqlite3.connect('news_app.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_topics (
            date TEXT PRIMARY KEY,
            topic1 TEXT,
            topic2 TEXT,
            topic3 TEXT
        )
    ''')
    # Ensure exactly three topics are saved (pad with empty strings if needed)
    topics = (topics + ["", "", ""])[:3]
    c.execute('''
        INSERT OR REPLACE INTO daily_topics (date, topic1, topic2, topic3)
        VALUES (?, ?, ?, ?)
    ''', (date_str, topics[0], topics[1], topics[2]))
    conn.commit()
    conn.close()

def main():
    # Define the date range: last six months until yesterday
    end_date = datetime.date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=2)
    current_date = start_date
    total_days = (end_date - start_date).days + 1
    print(f"Processing {total_days} days of news topics from {start_date} to {end_date}...")
    
    while current_date <= end_date:
        date_str = current_date.isoformat()
        print(f"\nProcessing date: {date_str}")
        
        news_text = fetch_news_for_date(date_str)
        if not news_text:
            print("  No news data fetched.")
            current_date += timedelta(days=1)
            continue
        
        keywords = extract_keywords_rake(news_text)
        top_keywords = get_top_three_keywords(keywords)
        if top_keywords:
            print("  Top topics:", top_keywords)
        else:
            print("  No topics extracted.")
            top_keywords = ["", "", ""]
        
        save_topics_to_db(date_str, top_keywords)
        print("  Topics saved to database.")
        current_date += timedelta(days=1)

if __name__ == "__main__":
    main()
