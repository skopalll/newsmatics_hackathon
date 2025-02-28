#!/usr/bin/env python3
import requests

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
    "published_on": "2025-02-26",
    "limit": 3,
    "language": "en"
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
            title = article.get("title")
            description = article.get("description")
            url = article.get("url")
            published_at = article.get("published_at")

            print(f"Title       : {title}")
            print(f"Description : {description}")
            print(f"URL         : {url}")
            print(f"Published at: {published_at}")
            print("-" * 40)
    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching the headlines:", e)

if __name__ == "__main__":
    fetch_top_headlines()
