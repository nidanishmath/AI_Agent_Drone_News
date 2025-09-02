# 📖 AI News Agent (Drone Industry)
## Overview

This project automates the full pipeline of discovering, summarizing, formatting, and posting drone-related news articles to social media (LinkedIn/X). It runs daily at 09:00 AM IST and reduces manual effort by turning raw news into engaging, ready-to-post content.

## 🔄 Workflow Steps
1. News Discovery

- Input: Keywords like “latest drone news”, “UAV technology”, “DGCA drones India”.
- Tool: Google News RSS / NewsAPI.
- Output: 3–5 latest articles with title, link, date, and image.

2. Summarization

- Tool: ChatGPT API / Taskade Writer.
- Process: Each article is summarized into 2–3 short paragraphs.
- Output: Concise summary, hashtags (e.g., #DroneTech, #UAV), and trending keywords.

3. Content Formatting

- Tool: Taskade AI / n8n text generator.
- Process: Convert summaries into social captions.
- Output:
    - Hook line
    - 1–2 line takeaway
    - Hashtags
    - Call-to-Action + Article link
    - Image reference

4. Social Auto-Posting

- Tool: LinkedIn API / Twitter API via n8n or Make.
- Output: Automatic posting of text + image at 09:00 AM IST.

## 📊 User Flow

- Scheduler triggers agent at 09:00 AM IST.
- News Discovery Agent fetches top 3–5 articles.
- AI Summarization Agent creates summaries + hashtags.
- Content Formatter Agent generates social-ready posts.
- Auto-Posting Agent publishes directly to LinkedIn/X.
- Admin (optional) receives a daily report of posts made.

## ⚙️ Tools & APIs Used

- Python → Workflow automation.
- Google News RSS / NewsAPI → News aggregation.
- Hugging Face Transformers → Summarization + formatting.
- LinkedIn API, Twitter API → Social auto-posting.

## 🛠️ Deployment Notes

- Schedule is set via CRON (0 9 * * *, Asia/Kolkata).
- Secrets/API keys stored securely in platform environment variables.
- De-duplication logic avoids reposting the same article.
- Logs are maintained in Google Sheets/Airtable for tracking post success/failure.

**✅ With this setup, the agent runs hands-free every day, keeps content fresh, and ensures a professional LinkedIn/Twitter presence in the drone/UAV space.**
