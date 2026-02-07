import os
from googleapiclient.discovery import build
import pandas as pd

# ✅ Read API key from environment (SAFE)
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise RuntimeError("YOUTUBE_API_KEY environment variable not set")

youtube = build("youtube", "v3", developerKey=API_KEY)


def get_channel_details(channel_id):
    response = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    ).execute()

    if "items" not in response or not response["items"]:
        return None

    item = response["items"][0]

    return {
        "channel_id": channel_id,
        "channel_name": item["snippet"]["title"],
        "subscribers": int(item["statistics"].get("subscriberCount", 0)),
        "total_views": int(item["statistics"].get("viewCount", 0)),
        "video_count": int(item["statistics"].get("videoCount", 0))
    }


def get_video_ids(channel_id, max_results=20):
    response = youtube.search().list(
        part="id",
        channelId=channel_id,
        maxResults=max_results,
        order="date",
        type="video"
    ).execute()

    return [
        item["id"]["videoId"]
        for item in response.get("items", [])
    ]


def get_video_details(video_ids):
    if not video_ids:
        return pd.DataFrame()

    response = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    ).execute()

    data = []
    for item in response.get("items", []):
        data.append({
            "video_id": item["id"],
            "title": item["snippet"]["title"],
            "publish_date": item["snippet"]["publishedAt"],
            "views": int(item["statistics"].get("viewCount", 0)),
            "likes": int(item["statistics"].get("likeCount", 0)),
            "comments": int(item["statistics"].get("commentCount", 0))
        })

    return pd.DataFrame(data)
