#!/usr/bin/env python3
"""
download_topics_historical.py

This script iterates over each day in the last six months, fetches U.S. news articles 
for that day from News API, aggregates the headlines and descriptions into a single text blob,
sends the blob to MeaningCloud’s Topic Extraction API to extract topics, selects the top three 
topics by relevance, and saves the results in a SQLite database.

Note: The News API free tier generally only provides recent articles (about one month back). 
For six months of data, you might need a paid plan or an alternative API.
"""

import requests
import sqlite3
import datetime
from datetime import timedelta

# Replace these with your actual API keys
NEWS_API_KEY = '6e2b2763e36547f187b7a6669d0ddd27'
MEANINGCLOUD_API_KEY = 'your_meaningcloud_api_key'

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
        'pageSize': 5  # maximum articles per request
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching news for {date_str}: {e}")
        return ""
    
    data = response.json()
    articles = data.get('articles', [])
    
    # Aggregate the title and description from each article.
    aggregated_text = " ".join(
        f"{article.get('title', '')} {article.get('description', '')}"
        for article in articles
    )
    return aggregated_text

def extract_topics(text):
    """
    Uses MeaningCloud’s Topic Extraction API to extract topics from the text.
    Returns a list of topics (each as a dict with keys like 'form' and 'relevance').
    """
    if not text.strip():
        return []
    
    url = 'https://api.meaningcloud.com/topics-2.0'
    payload = {
        'key': MEANINGCLOUD_API_KEY,
        'lang': 'en',
        'txt': text,
        'tt': 'a'  # 'a' extracts all topic types
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("Error extracting topics:", e)
        return []
    
    # MeaningCloud might return topics in "entity_list" or "concept_list"
    topics = data.get('entity_list', []) + data.get('concept_list', [])
    return topics

def get_top_three_topics(topics):
    """
    Sorts topics by their 'relevance' score and returns the top three topic names.
    """
    if not topics:
        return []
    # Sort topics by 'relevance'. If not present, default to 0.
    sorted_topics = sorted(topics, key=lambda t: float(t.get('relevance', 0)), reverse=True)
    top_three = sorted_topics[:3]
    top_topic_names = [topic.get('form', '').strip() for topic in top_three if topic.get('form')]
    return top_topic_names

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
    # Ensure we have exactly three topics (fill with empty strings if necessary)
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
    start_date = end_date - timedelta(days=180)  # roughly six months
    
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
        
        topics = extract_topics(news_text)
        top_topics = get_top_three_topics(topics)
        if top_topics:
            print("  Top topics:", top_topics)
        else:
            print("  No topics extracted.")
            top_topics = ["", "", ""]
        
        save_topics_to_db(date_str, top_topics)
        print("  Topics saved to database.")
        current_date += timedelta(days=1)

if __name__ == "__main__":
    main()
