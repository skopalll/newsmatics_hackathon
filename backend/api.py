import requests
from helpers import log, add_topic
from config import API_BASE_URL, API_TOKEN
import urllib.parse
import os

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}


def fetch_article_by_title(query_phrase):
    """
    Fetches an article from the API by searching for the query phrase
    in the article title (and text). Returns a dictionary with the article's
    published_date, title, and text if found.
    """
    # URL-encode the query phrase
    encoded_query = urllib.parse.quote(query_phrase)
    
    # Build URL with filter[query] and include-text=1
    url = f"{API_BASE_URL}/articles?filter%5Bquery%5D={encoded_query}&include-text=1&include-ownership=1"
    log(f"Requesting URL: {url}")
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        if not articles:
            log(f"No articles found for query: {query_phrase}")
            return None

        article = None
        for aux in articles:
            if aux.get("title") == query_phrase:
                article = aux

        if article is None:
            return None
        title = article.get("title", "No Title")
        published_date = article.get("published_at", "")
        text_content = article.get("text", "")  # Full text if available

        city = article.get("ownership", {}).get("publication_city", "Unknown City")
        state = article.get("ownership", {}).get("publication_state", "Unknown State")

        # Fallback to abstract if full text isn't available
        if not text_content:
            text_content = article.get("abstract", "")

        log(f"Fetched article: {title}")
        return {
            "published_date": published_date,
            "title": title,
            "text": text_content,
            "city": city,
            "state": state
        }
    except requests.exceptions.RequestException as e:
        log(f"Error fetching article: {str(e)}")
        return None

def fetch_and_store_article(title):
    
    article = fetch_article_by_title(title)
    if article:
        add_topic(article["published_date"], article["title"], article["text"])
        return article
    else:
        log("No article stored due to no match found.")
        return None





# TOHLE JE MOZNA STRASNY BS, CHATGPT HALUCINACE
def make_request(endpoint, params=None):
    """Helper function to make API requests"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        log(f"Successful request: {url}")
        return response.json()
    except requests.exceptions.RequestException as e:
        log(f"API request error: {str(e)}", "error")
        return None

def search_articles(query=None, start_date=None, end_date=None, page_size=10, include_ownership=0):
    """Search articles based on filters"""
    params = {"page[size]": page_size, "include-ownership": include_ownership}
    if query:
        params["filter[query]"] = query
    if start_date:
        params["filter[start-date]"] = start_date
    if end_date:
        params["filter[end-date]"] = end_date
    return make_request("/articles", params)

def get_article_counts(group_by="day", query=None, start_date=None, end_date=None):
    """Get article counts grouped by a specific period"""
    params = {"group-by": group_by}
    if query:
        params["filter[query]"] = query
    if start_date:
        params["filter[start-date]"] = start_date
    if end_date:
        params["filter[end-date]"] = end_date
    return make_request("/articles/counts", params)

def search_publications(query, page_size=10):
    """Search for publications using a query"""
    if len(query) < 2:
        log("Query must have at least 2 characters", "warning")
        return None
    params = {"filter[query]": query, "page[size]": page_size}
    return make_request("/publications", params)

def get_publication_details(publication_id, include_ownership=0):
    """Retrieve publication details by ID"""
    params = {"include-ownership": include_ownership}
    return make_request(f"/publications/{publication_id}", params)

def get_global_stats():
    """Get global statistics on articles, publications, and sources"""
    return make_request("/stats/global")
