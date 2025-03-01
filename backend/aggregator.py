import requests
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from config import API_TOKEN, BANNED, BANNED_REV, KEYWORDS, API_BASE_URL
from helpers import add_topic, add_article, connect_db
from localize import get_coordinates, get_publisher_latlong
import datetime
from random import randint


CLUSTER_COUNT = 150

def get_articles(date, max_articles=100000):
    
    articles = []
    params = {
        "filter[start-date]": date,
        "filter[end-date]": date,
        "page[size]": 1000,
        "include-text": 0,
        "include-ownership": 1 
    }

    # recommended
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    url = f"{API_BASE_URL}/api/v1/articles"

    # querying keywords disjunctively
    if KEYWORDS:
        params["filter[query]"] = " | ".join(["\"" + word + "\"" for word in KEYWORDS])

    # max articles is a helper for testing 
    while url and len(articles) < max_articles:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching articles: {response.status_code}")
            break
        
        data = response.json()
        batch_articles = data.get("articles", [])
        
        # Filter for articles published in the United States
        # with all relevant info needed for processing
        # that are credible and not irelevant
        filtered_articles = [
            article for article in batch_articles 
            if article.get("ownership", {}).get("publication_country") == "United States" 
            and article.get("published_at", "none") != "none"
            and (article.get("ownership", {}).get("publication_state", "idk") != "idk" or article.get("ownership", {}).get("publication_city", "idk") != "idk")
            and (article.get("credibility") == "ok") and (article.get("classification") != "Neutral" or (article.get("classification") == "Neutral" and randint(0,1) == 1))
        ]
        
        articles.extend(filtered_articles)
        
        print(f"Fetched {len(batch_articles)} articles; {len(filtered_articles)} matched filter; total so far: {len(articles)}")
        
        next_path = data.get("pagination", {}).get("next")
        url = API_BASE_URL + next_path if next_path else None
    
    return articles

def cluster_articles(articles, num_clusters=CLUSTER_COUNT):

    titles = [article.get("title") +  " : " + article.get("abstract") for article in articles]
    if not titles:
        # horrible fallback
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
    sorted_clusters = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)
    return [cluster for cluster, _ in sorted_clusters[:top_n]]

def get_most_relevant_articles(kmeans, clusters, articles, X):
    # most relevant article is basically the one in the middle of the cluster heap 
    # we do some basic checking to not get any bs article as the main headline
    relevant_articles = {}
    for cluster_label, indices in clusters.items():
        centroid = kmeans.cluster_centers_[cluster_label]
        best_idx = None
        valid_titles = []

        for idx in indices:
            vec = X[idx].toarray().flatten()
            distance = np.linalg.norm(vec - centroid)
            title = articles[idx].get("title", "")
            
            valid_titles.append((idx, distance, title))

        # Sort articles by distance to centroid (closest first)
        valid_titles.sort(key=lambda x: x[1])
        
        # no bs headline
        for idx, distance, title in valid_titles:
            if len(title) >= 8:
                best_idx = idx
                break
        
        # another horrible fallback, but it works 
        if best_idx is None and valid_titles:
            best_idx = valid_titles[0][0]

        if best_idx is not None:
            relevant_articles[cluster_label] = articles[best_idx]

    return relevant_articles


## DEBUGING FUNCTION
##---------------------------------------------
def print_cluster_details(kmeans, vectorizer, relevant_articles, clusters):
    feature_names = vectorizer.get_feature_names_out()
    sorted_clusters = sorted(clusters.items(), key=lambda item: len(item[1]), reverse=True)
    sorted_clusters = sorted_clusters[:10]

    for cluster_label, indices in sorted_clusters:
        centroid = kmeans.cluster_centers_[cluster_label]
        top_indices = centroid.argsort()[::-1][:5]  
        top_terms = [feature_names[i] for i in top_indices]
        useless = False
        for term in top_terms:
            if term in BANNED:
                useless = True
                break
        if useless:
            continue
        relevant_article = relevant_articles.get(cluster_label, {}).get("title", "No article")
        
        print(f"\nCluster {cluster_label+1}:")
        print(f"  Number of articles: {len(indices)}")
        print(f"  Top terms: {', '.join(top_terms)}")
        print(f"  Most relevant article: {relevant_article}")
##---------------------------------------------------------------------------

def extract_articles_from_clusters(articles, clusters, top_clusters):
    # getting articles from top clusters so we can put them in a db
    extracted_articles = []
    for cluster_label in top_clusters:
        aux = []
        for idx in clusters[cluster_label]:
            article = articles[idx]
            aux.append((
                article.get("publisher"),
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
    # helper functions have a lot of latency and overhead 
    conn = connect_db()
    cursor = conn.cursor()

    for days_ago in range(10, 1, -1):
        day = datetime.date.today() - datetime.timedelta(days=days_ago)
        date_str = day.strftime("%Y-%m-%d")
        articles = get_articles(date_str)

        if not articles:
            print("No articles retrieved.")
            return
        
        kmeans, vectorizer, clusters, _, X = cluster_articles(articles, num_clusters=CLUSTER_COUNT)
        
        if not clusters:
            print("No clustering was performed.")
            return
        
        relevant_articles = get_most_relevant_articles(kmeans, clusters, articles, X)
        top_clusters = get_top_clusters(clusters, top_n=10)
        
        #DEBUG
        # print_cluster_details(kmeans, vectorizer, relevant_articles, clusters)
        
        extracted_data = extract_articles_from_clusters(articles, clusters, top_clusters)

        valid_articles = 0
        for i in range(2,10):
            if valid_articles == 3:
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
            valid_articles += 1
            print(headline)
            count = 0
            topic_id = add_topic(date_str, headline, ";".join(top_terms))
            for id, time, city, state, title, cred, bias, url in extracted_data[i]:
                if count % 100 == 0:
                    print(f"processed articles {count}")
                count += 1
                coords = get_coordinates(city, state)

                # geopy fallback, but it was too slow
                # if not coords:
                #     coords = get_publisher_latlong(city, state)

                if coords and time: 
                    lat, long = coords
                    cursor.execute('''INSERT INTO articles (article_id, topic_id, title, time, politics, credibility, latitude, longitude, url)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (id, topic_id, title, time, bias, cred, lat, long, url))
            conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
