import os
import requests
import feedparser

LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

feeds = [
    (
        "台灣重大新聞",
        "https://news.google.com/rss?hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
        5,
    ),
    (
        "國際新聞",
        "https://news.google.com/rss/search?q=world+news&hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
        3,
    ),
]

# 過濾不太重要的新聞
skip_keywords = [
    "大學排名",
    "台灣人壽",
    "保險",
    "火鍋",
    "觀光",
    "旅遊",
    "演唱會",
    "優惠",
    "餐廳",
    "住宿",
    "飯店",
    "龍舟",
    "美食",
]

message_parts = ["📰 今日新聞摘要"]

for section_name, feed_url, max_count in feeds:

    message_parts.append("")
    message_parts.append(f"【{section_name}】")

    feed = feedparser.parse(feed_url)

    count = 0

    for entry in feed.entries:

        title = entry.title.split(" - ")[0]

        # 過濾雜訊新聞
        if any(word in title for word in skip_keywords):
            continue

        # 標題太長就縮短
        if len(title) > 35:
            title = title[:35] + "..."

        count += 1
        message_parts.append(f"{count}. {title}")

        if count >= max_count:
            break

message = "\n".join(message_parts)

print(message)

if not LINE_TOKEN:
    raise RuntimeError("缺少 LINE_CHANNEL_ACCESS_TOKEN")

if not LINE_USER_ID:
    raise RuntimeError("缺少 LINE_USER_ID")

response = requests.post(
    "https://api.line.me/v2/bot/message/push",
    headers={
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json",
    },
    json={
        "to": LINE_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message[:4900],
            }
        ],
    },
    timeout=30,
)

response.raise_for_status()

print("LINE 推播成功")
