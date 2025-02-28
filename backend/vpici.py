import requests
import urllib.parse
import time
import logging
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import numpy as np

# === Configuration ===
API_BASE_URL = "https://www.newsmatics.com/news-index/api/v1"
API_TOKEN = "YOUR_API_TOKEN_HERE"  # Replace with your actual API token
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# Maximum number of articles per request (max allowed: 1000)
PAGE_SIZE = 1000

# Logging setup
logging.basicConfig(
    filename="news_aggregator.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# === Helper Functions ===

def fetch_articles_for_date(date_str):
    """
    Fetches all articles for a specific date (format "YYYY-MM-DD")
    using the /articles endpoint.
    Returns a list of articles.
    """
    articles = []
    # Build the initial URL with date filters; note that both start and end dates are the same
    params = {
        "filter[start-date]": date_str,
        "filter[end-date]": date_str,
        "page[size]": PAGE_SIZE,
        "include-text": 1  # Include full text if available
    }
    # URL-encode parameters with square brackets already encoded
    query_string = "&".join([f"{urllib.parse.quote_plus(k)}={urllib.parse.quote_plus(str(v))}" for k, v in params.items()])
    url = f"{API_BASE_URL}/articles?{query_string}"
    logging.info(f"Fetching articles for {date_str} starting at URL: {url}")
    
    while url:
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            batch = data.get("articles", [])
            articles.extend(batch)
            logging.info(f"Fetched {len(batch)} articles; total so far: {len(articles)}")
            
            # Check if pagination indicates a next page
            pagination = data.get("pagination", {})
            next_url_path = pagination.get("next")
            if next_url_path:
                # Construct the full URL for the next page (assuming same base)
                url = f"{API_BASE_URL}{next_url_path}"
                # To be safe, pause briefly between requests to avoid rate limits
                time.sleep(1)
            else:
                url = None
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching articles: {e}")
            break

    return articles

def cluster_articles(articles, num_clusters=20):
    """
    Clusters articles based on their titles using SentenceTransformer embeddings and KMeans.
    Returns a list of clusters; each cluster is a dict with keys:
      - 'centroid_index': index of the representative article
      - 'cluster_size': number of articles in the cluster
      - 'indices': list of article indices belonging to the cluster
    """
    # Extract titles (or use title + abstract if desired)
    titles = [article.get("title", "") for article in articles]
    if not titles:
        logging.warning("No titles found for clustering.")
        return []
    
    # Generate embeddings for all titles
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(titles, show_progress_bar=True)
    
    # Run KMeans clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(embeddings)
    
    clusters = {}
    for idx, label in enumerate(cluster_labels):
        clusters.setdefault(label, []).append(idx)
    
    aggregated_clusters = []
    # For each cluster, find the article closest to the centroid
    for label, indices in clusters.items():
        cluster_embeddings = [embeddings[i] for i in indices]
        centroid = np.mean(cluster_embeddings, axis=0).reshape(1, -1)
        closest_idx, _ = pairwise_distances_argmin_min(centroid, cluster_embeddings)
        rep_index = indices[closest_idx[0]]
        aggregated_clusters.append({
            "centroid_index": rep_index,
            "cluster_size": len(indices),
            "indices": indices
        })
    return aggregated_clusters

def aggregate_headlines(date_str, num_clusters=20, top_n=3):
    """
    Fetches articles for the given date, clusters them, and returns the top_n clusters
    (by number of articles) with their representative headlines.
    """
    articles = fetch_articles_for_date(date_str)
    if not articles:
        logging.info("No articles fetched.")
        return []
    
    clusters = cluster_articles(articles, num_clusters=num_clusters)
    # Sort clusters by cluster_size in descending order
    clusters_sorted = sorted(clusters, key=lambda c: c["cluster_size"], reverse=True)
    
    top_clusters = clusters_sorted[:top_n]
    aggregated_headlines = []
    for cluster in top_clusters:
        rep_idx = cluster["centroid_index"]
        rep_title = articles[rep_idx].get("title", "No Title")
        published_at = articles[rep_idx].get("published_at", "")
        aggregated_headlines.append({
            "title": rep_title,
            "published_at": published_at,
            "coverage": cluster["cluster_size"]
        })
    return aggregated_headlines

# === Main Execution ===

if __name__ == "__main__":
    # Example: Aggregate headlines for a specific date (format: YYYY-MM-DD)
    target_date = "2025-02-27"  # Replace with your desired date
    logging.info(f"Aggregating headlines for {target_date}")
    
    top_headlines = aggregate_headlines(target_date, num_clusters=20, top_n=3)
    
    if top_headlines:
        print("Top Aggregated Headlines/Events:")
        for idx, item in enumerate(top_headlines, 1):
            print(f"{idx}. {item['title']}")
            print(f"   Published At: {item['published_at']}")
            print(f"   Coverage: {item['coverage']} articles")
    else:
        print("No aggregated headlines found for the given date.")
