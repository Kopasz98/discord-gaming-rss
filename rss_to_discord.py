import feedparser
import requests
import json
import os

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

POSTED_FILE = "posted.json"

if os.path.exists(POSTED_FILE):
    with open(POSTED_FILE, "r") as f:
        posted = set(json.load(f))
else:
    posted = set()

for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:5]:
        link = entry.get("link")
        if link and link not in posted:
            data = {
                "content": f"🎮 **{entry.title}**\n{link}"
            }
            requests.post(WEBHOOK_URL, json=data)
            posted.add(link)

with open(POSTED_FILE, "w") as f:
    json.dump(list(posted), f)
