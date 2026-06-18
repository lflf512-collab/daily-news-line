import os
import requests
import feedparser

LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

feeds = [
    ("台灣新聞", "https://news.google.com/rss/search?q=台灣&hl=zh-TW&gl=TW&ceid=TW:zh-Hant", 10),
    ("國際新聞", "https://news.google.com/rss/search?q=國際&hl=zh-TW&gl=TW&ceid=TW:zh-Hant", 5),
]

message_parts = ["早安，這是今天的新聞摘要："]

for title, url, limit in feeds:
    message_parts.append(f"\n【{title}】")
    feed = feedparser.parse(url)

    for i, entry in enumerate(feed.entries[:limit], 1):
        message_parts.append(f"{i}. {entry.title}\n{entry.link}")

message = "\n".join(message_parts)

print(message)

if not LINE_TOKEN or not LINE_USER_ID:
    raise RuntimeError("缺少 LINE_CHANNEL_ACCESS_TOKEN 或 LINE_USER_ID")

response = requests.post(
    "https://api.line.me/v2/bot/message/push",
    headers={
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json",
    },
    json={
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": message[:4900]}],
    },
    timeout=20,
)

response.raise_for_status()
print("LINE 推播成功")
