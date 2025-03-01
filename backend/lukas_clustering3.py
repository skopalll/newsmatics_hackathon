import requests
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from config import API_TOKEN, BANNED, BANNED_REV
from helpers import add_topic, add_article, connect_db
from localize import get_coordinates, get_publisher_latlong
import datetime
# import spacy

# nlp = spacy.load("en_core_web_sm")
BASE_URL = "https://www.newsmatics.com/news-index/api/v1"
DOMAIN_PREFIX = "https://www.newsmatics.com/news-index"
CLUSTER_COUNT = 120

def get_articles(date, max_articles=10000):
    """
    Retrieve articles for a specific date using the /articles endpoint.
    Filters articles to only include those published in the United States.
    """
    articles = []
    params = {
        "filter[start-date]": date,
        "filter[end-date]": date,
        "page[size]": 1000,
        "include-text": 0,
        "include-ownership": 1  # Ensure ownership details are included
    }
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    url = f"{BASE_URL}/articles"
    
    while url and len(articles) < max_articles:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching articles: {response.status_code}")
            break
        
        data = response.json()
        batch_articles = data.get("articles", [])
        
        # Filter for articles published in the United States
        filtered_articles = [
            article for article in batch_articles 
            if article.get("ownership", {}).get("publication_country") == "United States" 
            and article.get("published_at", "none") != "none"
            and (article.get("ownership", {}).get("publication_state", "idk") != "idk" or article.get("ownership", {}).get("publication_city", "idk") != "idk")
        ]
        
        articles.extend(filtered_articles)
        
        print(f"Fetched {len(batch_articles)} articles; {len(filtered_articles)} matched filter; total so far: {len(articles)}")
        
        next_path = data.get("pagination", {}).get("next")
        url = DOMAIN_PREFIX + next_path if next_path else None
        
        # time.sleep(1)  # Respect API rate limits
    
    return articles
def augment_text(article):
    """
    Combines the article's title and abstract, then uses spaCy to extract 
    named entities (PERSON, ORG, GPE) and appends them to enrich the text.
    """
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
def cluster_articles(articles, num_clusters=CLUSTER_COUNT):
    """
    Cluster article titles using TF-IDF and k-means clustering.
    """
    titles = [article.get("title") +  " : " + article.get("abstract") for article in articles]
    if not titles:
        return None, None, None, None, None
    
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(titles)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    kmeans.fit(X)
    
    clusters = {}
    for idx, label in enumerate(kmeans.labels_):
        clusters.setdefault(label, []).append(idx)
    
    return kmeans, vectorizer, clusters, titles, X

def get_top_clusters(clusters, top_n=3):
    """
    Get the top N clusters sorted by the number of articles they contain.
    """
    sorted_clusters = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)
    return [cluster for cluster, _ in sorted_clusters[:top_n]]

def get_most_relevant_articles(kmeans, clusters, articles, X):
    """
    Find the most relevant article for each cluster (closest to centroid).
    Ensures the title is at least 8 characters long; otherwise, picks the next best.
    """
    relevant_articles = {}
    for cluster_label, indices in clusters.items():
        centroid = kmeans.cluster_centers_[cluster_label]
        best_idx = None
        best_distance = float('inf')
        valid_titles = []

        for idx in indices:
            vec = X[idx].toarray().flatten()
            distance = np.linalg.norm(vec - centroid)
            title = articles[idx].get("title", "")
            
            valid_titles.append((idx, distance, title))

        # Sort articles by distance to centroid (closest first)
        valid_titles.sort(key=lambda x: x[1])
        
        # Select the first article with a valid title (at least 8 characters)
        for idx, distance, title in valid_titles:
            if len(title) >= 8:
                best_idx = idx
                break
        
        # If no valid title found, pick the shortest available one
        if best_idx is None and valid_titles:
            best_idx = valid_titles[0][0]

        if best_idx is not None:
            relevant_articles[cluster_label] = articles[best_idx]

    return relevant_articles

def print_cluster_details(kmeans, vectorizer, relevant_articles, clusters):
    """
    Print details for each cluster including top terms, most relevant article, and size.
    """
    feature_names = vectorizer.get_feature_names_out()
    sorted_clusters = sorted(clusters.items(), key=lambda item: len(item[1]), reverse=True)
    sorted_clusters = sorted_clusters[:10]
    
    print("\nClusters sorted by importance (number of articles):")
    for cluster_label, indices in sorted_clusters:
        centroid = kmeans.cluster_centers_[cluster_label]
        top_indices = centroid.argsort()[::-1][:5]  # Get top 5 terms
        top_terms = [feature_names[i] for i in top_indices]
        useless = False
        for term in top_terms:
            if term in BANNED:
                useless = True
                break
        if useless:
            continue
        relevant_article = relevant_articles.get(cluster_label, {}).get("title", "No relevant article found")
        
        print(f"\nCluster {cluster_label+1}:")
        print(f"  Number of articles: {len(indices)}")
        print(f"  Top terms: {', '.join(top_terms)}")
        print(f"  Most relevant article: {relevant_article}")

def extract_articles_from_clusters(articles, clusters, top_clusters):
    """
    Extract relevant article details from the top clusters.
    Returns a list of tuples.
    """
    extracted_articles = []
    for cluster_label in top_clusters:
        aux = []
        for idx in clusters[cluster_label]:
            article = articles[idx]
            aux.append((
                article.get("id"),
                article.get("published_at"),
                article.get("ownership", {}).get("publication_city", "Unknown"),
                article.get("ownership", {}).get("publication_state", "Unknown"),
                article.get("title"),
                article.get("credibility", "Unknown"),
                article.get("classification", "Unknown"),
                article.get("url")
            ))
        extracted_articles.append(aux)
    return extracted_articles

def main():
    conn = connect_db()
    cursor = conn.cursor()

    for days_ago in range(15, 1, -1):
        day = datetime.date.today() - datetime.timedelta(days=days_ago)
        date_str = day.strftime("%Y-%m-%d")
        articles = get_articles(date_str)

        if not articles:
            print("No articles retrieved.")
            return
        
        kmeans, vectorizer, clusters, titles, X = cluster_articles(articles, num_clusters=CLUSTER_COUNT)
        
        if not clusters:
            print("No clustering was performed.")
            return
        
        relevant_articles = get_most_relevant_articles(kmeans, clusters, articles, X)
        top_clusters = get_top_clusters(clusters, top_n=10)
        # print_cluster_details(kmeans, vectorizer, relevant_articles, clusters)
        
        
        
        extracted_data = extract_articles_from_clusters(articles, clusters, top_clusters)
        art_count = 0
        for i in range(2,10):
            if art_count == 3:
                break
            label = top_clusters[i]
            feature_names = vectorizer.get_feature_names_out()
            centroid = kmeans.cluster_centers_[label]
            top_indices = centroid.argsort()[::-1][:5]  # Get top 5 terms
            top_terms = [feature_names[i] for i in top_indices]
            useless = False
            for term in top_terms:
                if term in BANNED:
                    useless = True
                    break
            
            headline = relevant_articles.get(label, {}).get("title", "No headline")
            for x in BANNED_REV:
                if x in headline.lower():
                    useless = True
            if useless:
                continue
            art_count += 1
            print(headline)
            count = 0
            topic_id = add_topic(date_str, headline, ";".join(top_terms))
            for id, time, city, state, title, cred, bias, url in extracted_data[i]:
                if count % 100 == 0:
                    print(f"processed articles {count}")
                count += 1
                coords = get_coordinates(city, state)
                # if not coords:
                #     coords = get_publisher_latlong(city, state)
                if coords and time:
                    # add_article(id, topic_id, title, time, coords, bias, cred, url)
                    lat, long = coords
                    # Correct number of placeholders in the INSERT statement
                    cursor.execute('''INSERT INTO articles (article_id, topic_id, title, time, politics, credibility, latitude, longitude, url)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (id, topic_id, title, time, bias, cred, lat, long, url))
            conn.commit()



    conn.close()
    
    # # print("\nExtracted articles for database insertion:")
    # #for cluster in extracted_data:
    # #    for article in cluster:
    # #        print(article)

    # return extracted_data  # Can be used for database insertion

if __name__ == "__main__":
    main()
