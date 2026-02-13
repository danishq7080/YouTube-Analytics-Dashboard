import sqlite3
import pandas as pd
from database import create_tables

DB_NAME = "youtube_analytics.db"


def load_data():
    # Ensure tables exist first
    create_tables()

    conn = sqlite3.connect(DB_NAME)

    try:
        channels = pd.read_sql("SELECT * FROM channels", conn)
    except:
        channels = pd.DataFrame()

    try:
        videos = pd.read_sql("SELECT * FROM videos", conn)
    except:
        videos = pd.DataFrame()

    conn.close()
    return channels, videos



def add_engagement_rate(videos_df):
    videos_df["engagement_rate"] = (
        (videos_df["likes"] + videos_df["comments"]) / videos_df["views"]
    ).fillna(0)
    return videos_df


def top_videos(videos_df, n=10):
    return videos_df.sort_values(by="views", ascending=False).head(n)


def channel_kpis(videos_df):
    return {
        "total_videos": len(videos_df),
        "avg_views": int(videos_df["views"].mean()),
        "avg_likes": int(videos_df["likes"].mean()),
        "avg_comments": int(videos_df["comments"].mean()),
        "avg_engagement_rate": round(videos_df["engagement_rate"].mean() * 100, 2)
    }


def upload_trend(videos_df):
    videos_df["publish_date"] = pd.to_datetime(videos_df["publish_date"])
    trend = videos_df.groupby(
        videos_df["publish_date"].dt.to_period("M")
    ).size()
    return trend.reset_index(name="video_count")
