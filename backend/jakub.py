#!/usr/bin/env python3
import requests
from api import fetch_and_store_article
from datetime import datetime, timedelta

# Replace with your actual API token from thenewsapi.com
API_TOKEN = "G8d9Gi1grtkPQGALm4MKlMlS70CusLEQouUlmPkP"

# The endpoint for top stories
URL = "https://api.thenewsapi.com/v1/news/top"

# Parameters:
# - locale: set to "us" to get only US news
# - published_on: specify the date in YYYY-MM-DD format (e.g. "2025-02-28")
# - limit: restrict the result to 3 articles
# - language: (optional) restrict to English articles
params = {
    "api_token": API_TOKEN,
    "locale": "us",
    "published_on": "2025-02-05",
    "limit": 3,
    "language": "en",
    "categories" : "science,politics,tech"
}

def fetch_top_headlines():
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()  # Raise an error for bad status codes

        data = response.json()
        articles = data.get("data", [])
        if not articles:
            print("No articles found for the given parameters.")
            return
        

        print("Top Headlines:")
        print("=" * 40)
        for article in articles:
            # print(article)
            title = article.get("title")
            
            print(f"Title       : {title}")
            fetch_and_store_article(title)
            print("[green] done [/green]")
            print("-" * 40)
    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching the headlines:", e)

if __name__ == "__main__":
    for i in range(30, 0, -1):
        date = date.today() - timedelta(days=i)
        params["published_on"] = date.strftime("%Y-%m-%d")
        fetch_top_headlines()
