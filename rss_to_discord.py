# -*- coding: utf-8 -*-
import feedparser
import requests
import json
import os
import hashlib

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

RSS_FEEDS = [
    "https://gamerant.com/feed/gaming/",
    "https://feeds.ign.com/ign/all",
    "https://kotaku.com/rss",
    "https://www.gamespot.com/feeds/mashup/",
    "https://www.gameinformer.com/rss.xml",
    "https://n4g.com/rss/news",
    "https://www.gamesradar.com/rss",
    "https://www.theverge.com/gaming/rss/index.xml",
    "https://www.techradar.com/rss",
    "https://www.engadget.com/rss.xml",
    "https://www.digitaltrends.com/gaming/feed/",
    "https://www.thegamer.com/feed/",
    "https://www.videogameschronicle.com/feed/",
    "https://www.pcgamer.com/rss/",
    "https://www.eurogamer.net/feed",
    "https://www.polygon.com/rss/index.xml",
    "https://www.rockpapershotgun.com/feed",
    "https://www.destructoid.com/feed/",
    "https://www.giantbomb.com/feeds/news/",
    "https://www.siliconera.com/feed/",
    "https://www.shacknews.com/rss",
    "https://www.gamezone.com/feed/",
    "https://rss.slashdot.org/Slashdot/slashdotGames",
    "https://gamefaqs.gamespot.com/feeds/news.xml",
    "https://www.dexerto.com/feed/",
    "https://stealthoptional.com/feed/",
    "https://siege.gg/rss",
    "https://racinggames.gg/feed/",
    "https://mtgrocks.com/feed/",
    "https://epicstream.com/feed",
    "https://www.bluesnews.com/feed/",
    "https://www.metacritic.com/rss/games",
    "https://www.gametrailers.com/rss",
    "https://www.neogaf.com/rss",
    "https://www.gamechannel.hu/feed",
    "https://prohardver.hu/hirfolyam/rss.html",
    "https://www.pcguru.hu/rss",
    "https://www.gamestar.hu/rss",
    "https://hu.ign.com/rss",
    "https://play3.hu/feed",
    "https://www.xboxhungary.net/feed",
    "https://www.playdome.hu/rss",
    "https://www.konzolvilag.hu/rss",
    "https://ultimateconsole.hu/feed",
    "https://felhokarcolo.hu/rss"

]

INCLUDE_KEYWORDS = [k.lower() for k in [
    "Battlefield 6", "Escape From Tarkov",
    "Solo Leveling", "Pacific Drive",
    "Palworld", "Overwatch 2", "GTA VI",
    "Fallout", "The Sims", "inZOI",
    "multiplayer", "battle royale",
    "Battlefield", "PUBG", "Fortnite",
    "Arc Raiders", "Elden Ring", "Peak", "Sea of Thieves",
    "Grand Theft Auto", "Helldivers 2", "Counter-Strike 2",
    "Apex Legends", "Destiny 2", "Call of Duty",
    "Rocket League", "Forza Horizon","Fable", "Diablo", "Pokemon", "Zelda", "FragPunk", "LEGO",
"Gran Turismo", "STAR WARS", "Far Cry", "Marvel Rivals","Ubisoft","Rockstar Games","Arc System Works","Subnautica",
    "Assassin's Creed", "Biotech Gameworks","CD Project Red","Cyberpunk","DayZ","Dying Light","Electronic Arts",
    "Epic Games","Respawn Entertainment","Fallout","Game Awards","GTA","Hello Games","io interactive","FromSoftware","Krafton",
    "Leslie Benzies","MindsEye","No Man's Sky","Overwatch","PlayerUnknown's Battlegrounds","Polyphony Digital","Rainbow Six Siege",
    "Raven Software","ready or not","Schedule 1","Sims","Snail Games","ARK","Techland","tekken","Tom Clancy's Rainbow Six Siege X",
    "Tyler's Video Game Studio","void interactive","EA Sports FC","Tomb Raider"
]]

EXCLUDE_KEYWORDS = [k.lower() for k in [
    "rumor", "leak", "unconfirmed",
    "giveaway", "free skins",
    "sale", "discount",
    "top 10", "best of",
    "opinion", "editorial","esport","free"
]]

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


posted = set()
if os.path.exists(POSTED_FILE):
    try:
        with open(POSTED_FILE, "r", encoding="utf-8") as f:
            posted = set(json.load(f))
    except Exception:
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
