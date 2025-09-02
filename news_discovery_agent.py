import requests
import feedparser
from datetime import datetime
from dotenv import load_dotenv
import os
import json

# --- CONFIG ---
load_dotenv()
NEWSAPI_KEY = os.getenv('NEWS_API_KEY')
KEYWORDS = ["latest drone news", "UAV technology", "DGCA drones India"]
MIN_ARTICLES, MAX_ARTICLES = 3, 5
PLACEHOLDER_IMAGE = "https://images.unsplash.com/photo-1487219116710-23ffcb172b2b?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTh8fGRyb25lfGVufDB8fDB8fHww"

# Fetch articles from NewsAPI
def fetch_from_newsapi():
    articles = []
    for keyword in KEYWORDS:
        url = f"https://newsapi.org/v2/everything?q={keyword}&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWSAPI_KEY}"
        r = requests.get(url).json()
        for a in r.get("articles", []):
            articles.append({
                "title": a.get("title"),
                "link": a.get("url"),
                "publishedAt": a.get("publishedAt"),
                "image": a.get("urlToImage") or PLACEHOLDER_IMAGE
            })
    return articles

# Fetch articles from Google News RSS
def fetch_from_google_rss():
    url = "https://news.google.com/rss/search?q=drone+UAV+India&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:MAX_ARTICLES]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "publishedAt": getattr(entry, "published", None),
            "image": PLACEHOLDER_IMAGE  # RSS often doesn’t provide images
        })
    return articles

# Aggregate, deduplicate, and limit results
def aggregate_articles():
    all_articles = fetch_from_newsapi() + fetch_from_google_rss()

    # Deduplicate by link
    seen, unique_articles = set(), []
    for art in sorted(all_articles, key=lambda x: x["publishedAt"] or "", reverse=True):
        if art["link"] not in seen:
            seen.add(art["link"])
            unique_articles.append(art)

    # Limit between MIN_ARTICLES and MAX_ARTICLES
    return unique_articles[:MAX_ARTICLES] if len(unique_articles) >= MIN_ARTICLES else unique_articles

articles = aggregate_articles()

# Save to JSON
with open("articles.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, indent=2, ensure_ascii=False)

# Print nicely
for a in articles:
    print(f"Title: {a['title']}")
    print(f"Link: {a['link']}")
    print(f"Published At: {a['publishedAt']}")
    print(f"Image: {a['image']}")
    print("-" * 50)
