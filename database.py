import sqlite3

DB_NAME = "youtube_analytics.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS channels (
        channel_id TEXT PRIMARY KEY,
        channel_name TEXT,
        subscribers INTEGER,
        total_views INTEGER,
        video_count INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        video_id TEXT PRIMARY KEY,
        channel_id TEXT,
        title TEXT,
        publish_date TEXT,
        views INTEGER,
        likes INTEGER,
        comments INTEGER
    )
    """)

    conn.commit()
    conn.close()


def insert_channel(channel):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO channels VALUES (?, ?, ?, ?, ?)
    """, (
        channel["channel_id"],
        channel["channel_name"],
        channel["subscribers"],
        channel["total_views"],
        channel["video_count"]
    ))

    conn.commit()
    conn.close()


def insert_videos(videos_df, channel_id):
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in videos_df.iterrows():
        cursor.execute("""
        INSERT OR REPLACE INTO videos VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            row["video_id"],
            channel_id,
            row["title"],
            row["publish_date"],
            row["views"],
            row["likes"],
            row["comments"]
        ))

    conn.commit()
    conn.close()
