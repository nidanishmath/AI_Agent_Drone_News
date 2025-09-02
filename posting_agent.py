# social_auto_posting_agent.py
import json
import tweepy
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Toggle this flag: True = test mode (print only), False = live posting
TEST_MODE = True  

# 🔑 Twitter (X) credentials
TW_CONSUMER_KEY = os.getenv("TW_CONSUMER_KEY")
TW_CONSUMER_SECRET = os.getenv("TW_CONSUMER_SECRET")
TW_ACCESS_TOKEN = os.getenv("TW_ACCESS_TOKEN")
TW_ACCESS_SECRET = os.getenv("TW_ACCESS_SECRET")

# 🔑 LinkedIn credentials
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_USER_ID = os.getenv("LINKEDIN_USER_ID")  # personal user id


def load_posts(file_path="social_posts.json"):
    """Load social posts from Step 3 output file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ------------------ TWITTER POST ------------------
def post_to_twitter(caption, image_url):
    if TEST_MODE:
        print("🟡 [TEST MODE] Twitter post preview:")
        print(caption)
        print("Image:", image_url)
        return

    client = tweepy.Client(
        consumer_key=TW_CONSUMER_KEY,
        consumer_secret=TW_CONSUMER_SECRET,
        access_token=TW_ACCESS_TOKEN,
        access_token_secret=TW_ACCESS_SECRET
    )

    media = None
    try:
        # Download image and upload to Twitter
        filename = "temp.jpg"
        img_data = requests.get(image_url).content
        with open(filename, "wb") as f:
            f.write(img_data)

        media = client.media_upload(filename)
        os.remove(filename)
    except Exception as e:
        print("⚠️ Could not upload image:", e)

    try:
        if media:
            client.create_tweet(text=caption, media_ids=[media.media_id])
        else:
            client.create_tweet(text=caption)
        print("✅ Posted to Twitter (X)")
    except Exception as e:
        print("❌ Twitter post failed:", e)


# ------------------ LINKEDIN POST ------------------
def post_to_linkedin(caption, image_url):
    if TEST_MODE:
        print("🟡 [TEST MODE] LinkedIn post preview:")
        print(caption)
        print("Image:", image_url)
        return

    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "author": f"urn:li:person:{LINKEDIN_USER_ID}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": caption},
                "shareMediaCategory": "ARTICLE",
                "media": [{"status": "READY", "originalUrl": image_url}]
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    try:
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code == 201:
            print("✅ Posted to LinkedIn")
        else:
            print("❌ LinkedIn post failed:", resp.text)
    except Exception as e:
        print("❌ LinkedIn API error:", e)


# ------------------ MAIN ------------------
def auto_post():
    posts = load_posts()

    for post in posts:
        caption = post["caption"]
        image = post["image"]

        print("\n🚀 Preparing to post:", post["title"])
        post_to_twitter(caption, image)
        post_to_linkedin(caption, image)


auto_post()
