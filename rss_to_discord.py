import feedparser
import requests
import json
import os
import hashlib

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

RSS_FEEDS = [
    "https://www.eurogamer.net/?format=rss",
    "https://kotaku.com/rss",
    "https://www.polygon.com/rss/index.xml",
    "http://feeds.ign.com/ign/all",
    "https://www.gamesindustry.biz/rss/gamesindustry_news_feed.rss",
    "https://store.steampowered.com/feeds/news.xml",
    "https://www.nintendolife.com/feeds/latest",
    "https://nintendoeverything.com/feed",
    "https://majornelson.com/feed/",
    "https://news.xbox.com/en-us/feed",
    "http://feeds.feedburner.com/psblog",
    "http://feeds.feedburner.com/RockPaperShotgun",
    "http://feeds.feedburner.com/GamasutraNews",
    "https://www.reddit.com/r/gaming.rss"
]

INCLUDE_KEYWORDS = [
    "steam", "playstation", "xbox", "nintendo",
    "pc", "console",
    "patch", "update", "release",
    "gpu", "hardware",
    "unity", "unreal",
    "esports", "indie"
]

EXCLUDE_KEYWORDS = [
    "rumor", "leak", "unconfirmed",
    "giveaway", "free skins",
    "sale", "discount",
    "top 10", "best of",
    "opinion", "editorial"
]

POSTED_FILE = "posted.json"


def is_relevant(entry):
    text = (
        entry.get("title", "") +
        " " +
        entry.get("summary", "")
    ).lower()

    if not any(keyword in text for keyword in INCLUDE_KEYWORDS):
        return False

    if any(keyword in text for keyword in EXCLUDE_KEYWORDS):
        return False

    return True


def entry_id(entry):
    base = entry.get("id") or entry.get("link") or entry.get("title", "")
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


if os.path.exists(POSTED_FILE):
    with open(POSTED_FILE, "r") as f:
        posted = set(json.load(f))
else:
    posted = set()

new_posts = []

for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:5]:
        if not is_relevant(entry):
            continue

        eid = entry_id(entry)
        if eid in posted:
            continue

        new_posts.append({
            "title": entry.title,
            "link": entry.link
        })

        posted.add(eid)

for post in new_posts:
    data = {
        "content": f"🎮 **{post['title']}**\n{post['link']}"
    }
    requests.post(WEBHOOK_URL, json=data)

with open(POSTED_FILE, "w") as f:
    json.dump(list(posted), f)
