import feedparser

feeds = [
    ("台灣新聞", "https://news.google.com/rss/search?q=台灣&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"),
    ("國際新聞", "https://news.google.com/rss/search?q=國際&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"),
]

for title, url in feeds:
    print(f"\n【{title}】")
    feed = feedparser.parse(url)
    limit = 10 if title == "台灣新聞" else 5

    for i, entry in enumerate(feed.entries[:limit], 1):
        print(f"{i}. {entry.title}")
        print(entry.link)
