import requests
from helpers import log
from config import API_BASE_URL, API_TOKEN
import os

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}


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
