import json
import tensorflow as tf
from transformers import pipeline
from newspaper import Article
from news_discovery_agent import fetch_from_newsapi, fetch_from_google_rss

# Load summarization pipeline

summarizer = pipeline("summarization", 
                      model="facebook/bart-large-cnn")

def fetch_article_text(url):
    """Fetch full article text using newspaper3k. Fallback to None if it fails."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception:
        return None

def extract_hashtags_and_keywords(summary_text):
    """
    Very simple keyword + hashtag extractor.
    You can replace this later with spaCy, KeyBERT, or YAKE for better results.
    """
    words = [w.strip(".,!?").lower() for w in summary_text.split()]
    keywords = list(set([w for w in words if len(w) > 5]))[:5]  # pick top 5
    hashtags = ["#" + k.capitalize() for k in keywords]
    return hashtags, keywords

def summarize_articles():
    # Step 1: Fetch articles from discovery agent
    newsapi_articles = fetch_from_newsapi()
    rss_articles = fetch_from_google_rss()
    combined = (newsapi_articles + rss_articles)[:5]  # Top 5

    with open("articles.json", "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    summaries = []
    for article in combined:
        text = fetch_article_text(article['link']) or article["title"]  # we only have title (not full content yet)
        if len(text.split()) < 30:
            summary_text = text
        else:
            try:
                summary = summarizer(
                    text, 
                    max_length=130, 
                    min_length=30, 
                    do_sample=False
                )
                summary_text = summary[0]["summary_text"]
            except Exception as e:
                summary_text = f"[Error summarizing: {e}]"


        # Step 3: Extract hashtags & keywords
        hashtags, keywords = extract_hashtags_and_keywords(summary_text)

        summaries.append({
            "title": article["title"],
            "link": article["link"],
            "publishedAt": article["publishedAt"],
            "summary": summary_text,
            "hashtags": hashtags,
            "keywords": keywords
        })
        
    # save into json for next step
    with open("summaries.json", "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=2, ensure_ascii=False)

    return summaries

results = summarize_articles()
for r in results:
    print("\n" + "-"*50)
    print("\nTitle:", r["title"])
    print("Published:", r["publishedAt"])
    print("Link:", r["link"])
    print("\nSummary:", r["summary"])
    print("\nHashtags:", ", ".join(r["hashtags"]))
    print("Keywords:", ", ".join(r["keywords"]))

