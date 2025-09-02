import streamlit as st
import json
from datetime import datetime
import pytz
import difflib

# Page Configuration
st.set_page_config(page_title="🚁 Drone News", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    /* Remove extra padding/whitespace in layout */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Remove gap between elements */
    .element-container {
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }

    /* Background Image */
    .stApp {
        background: url("https://images.unsplash.com/photo-1489087433598-048557455f41?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D") no-repeat center center fixed;
        background-size: cover;
    }

    /* Title */
    .title {
        font-size: 42px;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
        margin-bottom: 10px;
    }

    /* Subtitle */
    .subtitle {
        font-size: 20px;
        color: #f1f1f1;
        font-weight: 400;
        margin-bottom: 25px;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.5);
    }

    /* Article Card */
    .card {
        background-color: rgba(255, 255, 255, 0.92);
        padding: 20px 25px;
        border-radius: 16px;
        margin-bottom: 15px; /* nice small gap */
        box-shadow: 2px 4px 15px rgba(0,0,0,0.2);
    }

    /* Article Title */
    .article-title {
        font-size: 26px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 8px;
    }

    /* Metadata */
    .meta {
        font-size: 14px;
        color: #7f8c8d;
        margin-bottom: 12px;
    }

    /* Summary */
    .summary {
        font-size: 16px;
        color: #2c3e50;
        line-height: 1.6;
        margin-bottom: 12px;
    }

    /* Hashtags */
    .hashtags {
        font-size: 14px;
        font-weight: 500;
        color: #117A65;
    }
    </style>
""", unsafe_allow_html=True)


# Load JSON safely
def load_json(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning(f"{file} not found. Run the agent first.")
        return []

articles = load_json("articles.json")
summaries = load_json("summaries.json")
posts = load_json("social_posts.json")

# Convert UTC → IST
def convert_to_ist(utc_str):
    try:
        utc_dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        ist = pytz.timezone("Asia/Kolkata")
        return utc_dt.astimezone(ist).strftime("%d-%b-%Y %I:%M %p")
    except:
        return utc_str

# Helper: fuzzy title matching
def find_best_match(title, dataset):
    titles = [item["title"] for item in dataset]
    match = difflib.get_close_matches(title, titles, n=5, cutoff=0.5)
    if match:
        return next((item for item in dataset if item["title"] == match[0]), None)
    return None

# Title
st.markdown('<p class="title">🚁 Drone News AI</p>', unsafe_allow_html=True)

# Unified News Cards
st.markdown('<p class="subtitle">📰 Latest Drone News</p>', unsafe_allow_html=True)
for a in articles:
    # match summary by link (stronger match than title)
    summary = next((s for s in summaries if s.get("link") == a.get("link")), None)
    # match post by title (since social_posts.json has no link)
    post = next((p for p in posts if p.get("title") == a.get("title")), None)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        # Title
        st.markdown(f"### {a['title']}")

        # Date (IST)
        st.write(f"📅 **Published:** {convert_to_ist(a.get('publishedAt',''))}")

        # Link
        if a.get("link"):
            st.write(f"🔗 [Read Full News Here]({a['link']})")

        # Summary
        if summary:
            st.write(f"**📝 Summary:** {summary['summary']}")
            if summary.get("hashtags"):
                st.write("🔖 **Hashtags:**", ", ".join(summary["hashtags"]))
            if summary.get("keywords"):
                st.write("🔥 **Keywords:**", ", ".join(summary["keywords"]))
        else:
            st.write("⚠️ No summary available.")

        # Social Media Caption
        if post:
            st.write("**📲 Suggested Social Media Caption:**")
            st.markdown(f"> {post['caption']}")
            if post.get("image"):
                st.image(post["image"], width=500)

        # Article Image
        if a.get("image"):
            st.image(a["image"], use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)


print("Article example:", articles[0])
print("Summary example:", summaries[0])
print("Social post example:", posts[0])