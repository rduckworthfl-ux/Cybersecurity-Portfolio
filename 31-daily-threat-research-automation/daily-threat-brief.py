#!/usr/bin/env python3
"""Daily cybersecurity threat brief: RSS -> Gemini -> phone push."""

import os
import sys
import logging
import datetime
import feedparser
import requests
from google import genai

# --- Configuration --- #
FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.darkreading.com/rss.xml",
    "http://krebsonsecurity.com/feed/",
]
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "REPLACE_WITH_YOUR_OWN_TOPIC")
LOOKBACK_HOURS = 24
LOG_FILE = os.path.expanduser("~/projects/threat-brief/brief.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def pull_recent_articles(feed_urls, hours):
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=hours)
    collected = []
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ThreatBriefBot/1.0)"}
    for url in feed_urls:
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            parsed = feedparser.parse(resp.content)
            if parsed.bozo:
                logging.warning(f"Feed parse issue for {url}: {parsed.bozo_exception}")
            for entry in parsed.entries:
                pub_struct = entry.get("published_parsed") or entry.get("updated_parsed")
                if not pub_struct:
                    continue
                pub_dt = datetime.datetime(*pub_struct[:6], tzinfo=datetime.timezone.utc)
                if pub_dt > cutoff:
                    title = entry.get("title", "Untitled")
                    summary = entry.get("summary", "")
                    link = entry.get("link", "")
                    collected.append(f"{title}: {summary} (Source: {link})")
        except Exception as e:
            logging.error(f"Failed to fetch {url}: {e}")
    return collected


def build_prompt(articles):
    joined = "\n".join(articles)
    return f"""You are a Lead Threat Intelligence Analyst prepping a morning brief.
Analyze the following RSS titles, descriptions, and source links from the last 24 hours:

{joined}

Rules:
1. BLUF: 2-sentence urgent warning at the top for any major/nation-state/zero-day activity.
2. List up to 5 critical vulnerabilities/breaches, each with a 1-sentence impact and 1-sentence remediation.
3. After each item, add a new line: Source: [Read More](link)
4. Bold CVEs and threat actor names using double asterisks. Short sentences. No filler.
5. Use Markdown headers (##) for section titles instead of bold text for structure."""


def summarize_with_gemini(prompt_text):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY not set")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt_text,
    )
    return response.text


def push_to_phone(message, topic):
    resp = requests.post(
        f"https://ntfy.sh/{topic}",
        data=message.encode("utf-8"),
        headers={
            "Title": "Daily Threat Brief",
            "Markdown": "yes",
        },
        timeout=15,
    )
    resp.raise_for_status()


def main():
    articles = pull_recent_articles(FEEDS, LOOKBACK_HOURS)
    if not articles:
        logging.info("No new articles in the lookback window. Skipping.")
        return
    prompt = build_prompt(articles)
    brief = summarize_with_gemini(prompt)
    push_to_phone(brief, NTFY_TOPIC)
    logging.info(f"Brief sent successfully with {len(articles)} source articles.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Job failed: {e}")
        sys.exit(1)
