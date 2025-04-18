import requests
import urllib.parse
import time
import logging
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sklearn.metrics import pairwise_distances_argmin_min
import numpy as np
import spacy
import hdbscan
from sklearn.preprocessing import normalize
from config import API_BASE_URL, API_TOKEN

HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

PAGE_SIZE = 1000

# UNUSED MODEL TO AGGREGATE, good but really slow 50 min on laptop

# Load spaCy model for NER (make sure to run: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

def fetch_articles_for_date(date_str):
    articles = []
    params = {
        "filter[start-date]": date_str,
        "filter[end-date]": date_str,
        "page[size]": PAGE_SIZE,
        "include-text": 1,
        "include-ownership": 1
    }
    query_string = "&".join([f"{urllib.parse.quote_plus(k)}={urllib.parse.quote_plus(str(v))}" for k, v in params.items()])
    url = f"{API_BASE_URL}/api/v1/articles?{query_string}"
    logging.info(f"Fetching articles for {date_str} starting at URL: {url}")
    count = 1
    while url:
        try:
            if count == 10:
                break
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            batch = data.get("articles", [])
            for article in batch:
                ownership = article.get("ownership", {})
                pub_country = ownership.get("publication_country", "unknown")
                if pub_country == "United States":
                    articles.append(article)
            logging.info(f"Fetched {len(batch) * count} articles; total filtered so far: {len(articles)}")
            pagination = data.get("pagination", {})
            next_url_path = pagination.get("next")
            if next_url_path:
                url = f"{API_BASE_URL}{next_url_path}&include-text=1&include-ownership=1"
            else:
                url = None
            count += 1
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching articles: {e}")
            break

    return articles

def augment_text(article):
    title = article.get("title", "")
    abstract = article.get("abstract", "")
    combined_text = f"{title}. {abstract}"
    doc = nlp(combined_text)
    entities = [ent.text for ent in doc.ents if ent.label_ in {"PERSON", "ORG", "GPE"}]
    if entities:
        unique_entities = " ".join(set(entities))
        return combined_text + " " + unique_entities
    else:
        return combined_text

def cluster_articles(articles):
    texts = [augment_text(article) for article in articles]
    if not texts:
        logging.warning("No texts found for clustering.")
        return []
    
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, show_progress_bar=True)
    
    embeddings = normalize(embeddings, norm='l2')
    
    clusterer = hdbscan.HDBSCAN(min_cluster_size=3, min_samples=2, metric='euclidean')
    cluster_labels = clusterer.fit_predict(embeddings)
    
    clusters = {}
    for idx, label in enumerate(cluster_labels):
        if label == -1:
            continue  # skip noise
        clusters.setdefault(label, []).append(idx)
    
    aggregated_clusters = []
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

def aggregate_headlines(date_str, top_n=3):
    articles = fetch_articles_for_date(date_str)
    if not articles:
        logging.info("No articles fetched.")
        return []
    
    clusters = cluster_articles(articles)
    clusters_sorted = sorted(clusters, key=lambda c: c["cluster_size"], reverse=True)
    top_clusters = clusters_sorted[:top_n]
    
    aggregated_headlines = []
    for cluster in top_clusters:
        rep_idx = cluster["centroid_index"]
        rep_title = articles[rep_idx].get("title", "No Title")
        published_at = articles[rep_idx].get("published_at", "")
        aggregated_headlines.append({
            "headline": rep_title,
            "published_at": published_at,
            "coverage": cluster["cluster_size"]
        })
    return aggregated_headlines

if __name__ == "__main__":

    target_date = "2024-11-05"  # Replace with your desired date
    logging.info(f"Aggregating headlines for {target_date}")
    
    top_headlines = aggregate_headlines(target_date, top_n=3)
    
    if top_headlines:
        print("Top Aggregated Headlines/Events:")
        for idx, item in enumerate(top_headlines, 1):
            print(f"{idx}. {item['headline']}")
            print(f"   Published At: {item['published_at']}")
            print(f"   Coverage: {item['coverage']} articles")
    else:
        print("No aggregated headlines found for the given date.")
