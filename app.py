import streamlit as st
import matplotlib.pyplot as plt
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build

from youtube_api import API_KEY, get_channel_details, get_video_ids, get_video_details
from database import create_tables, insert_channel, insert_videos
from analytics import load_data, add_engagement_rate, top_videos, channel_kpis, upload_trend

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="YouTube Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main {
    padding-top: 1.5rem;
}
h1, h2, h3 {
    color: #ffffff;
}
.metric-card {
    background: #1f2937;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.metric-title {
    color: #9ca3af;
    font-size: 14px;
}
.metric-value {
    color: #ffffff;
    font-size: 28px;
    font-weight: bold;
}
.section {
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

youtube_client = build("youtube", "v3", developerKey=API_KEY)

# ---------------- HELPER ----------------
def extract_channel_id(text):
    text = text.strip()

    if "youtube.com/channel/" in text:
        return text.split("channel/")[-1].split("/")[0]

    if "youtube.com/@" in text:
        handle = text.split("@")[-1]
        res = youtube_client.search().list(
            part="snippet", q=handle, type="channel", maxResults=1
        ).execute()
        if res.get("items"):
            return res["items"][0]["snippet"]["channelId"]

    if "youtu.be" in text or "watch?v=" in text:
        if "youtu.be" in text:
            vid = text.split("/")[-1].split("?")[0]
        else:
            vid = parse_qs(urlparse(text).query).get("v", [None])[0]

        if vid:
            res = youtube_client.videos().list(
                part="snippet", id=vid
            ).execute()
            if res.get("items"):
                return res["items"][0]["snippet"]["channelId"]

    return text

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>📊 YouTube Analytics & Insight Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#9ca3af;'>Analyze YouTube channel performance using real-time data</p>", unsafe_allow_html=True)

st.divider()

# ---------------- INPUT SECTION ----------------
col_left, col_mid, col_right = st.columns([1, 3, 1])

with col_mid:
    channel_input = st.text_input(
        "🔗 YouTube Channel / Video URL / Channel ID",
        placeholder="https://www.youtube.com/@GoogleDevelopers"
    )
    fetch = st.button("🚀 Fetch Channel Data", use_container_width=True)

if fetch and channel_input:
    channel_id = extract_channel_id(channel_input)

    with st.spinner("Fetching data from YouTube..."):
        create_tables()
        channel = get_channel_details(channel_id)

        if channel:
            insert_channel(channel)
            videos_df = get_video_details(get_video_ids(channel_id))
            insert_videos(videos_df, channel_id)
            st.success("✅ Channel data fetched successfully!")
            st.rerun()

        else:
            st.error("❌ Invalid YouTube link or channel")

# ---------------- LOAD DATA ----------------
channels_df, videos_df = load_data()

if videos_df.empty:
    st.info("ℹ️ Enter a YouTube channel above to see analytics.")
    st.stop()

videos_df = add_engagement_rate(videos_df)
kpis = channel_kpis(videos_df)

# ---------------- KPI CARDS ----------------
st.markdown("<div class='section'></div>", unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns(5)

def metric(col, title, value):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

metric(k1, "📹 Videos", kpis["total_videos"])
metric(k2, "👀 Avg Views", kpis["avg_views"])
metric(k3, "👍 Avg Likes", kpis["avg_likes"])
metric(k4, "💬 Avg Comments", kpis["avg_comments"])
metric(k5, "🔥 Engagement %", f'{kpis["avg_engagement_rate"]}%')

# ---------------- TOP VIDEOS ----------------
st.markdown("<div class='section'></div>", unsafe_allow_html=True)
st.subheader("🏆 Top Performing Videos")

top_df = top_videos(videos_df)
st.dataframe(
    top_df[["title", "views", "likes", "comments", "engagement_rate"]],
    use_container_width=True
)

# ---------------- CHARTS (COMPACT) ----------------
# st.markdown("<div class='section'></div>", unsafe_allow_html=True)

# left, mid, right = st.columns([1, 2, 1])

# with mid:
#     st.subheader("📊 Quick Trends")

#     # Smaller Views per Video
#     st.caption("📈 Views per Video")
#     fig1, ax1 = plt.subplots(figsize=(1,2))
#     ax1.bar(top_df["title"], top_df["views"], color="#4f46e5")
#     ax1.tick_params(axis="x", rotation=45)
#     ax1.set_ylabel("Views")
#     st.pyplot(fig1, use_container_width=True)

#     # Smaller Upload Trend
#     st.caption("📅 Upload Trend (Monthly)")
#     trend_df = upload_trend(videos_df)
#     fig2, ax2 = plt.subplots(figsize=(1, 2))
#     ax2.plot(
#         trend_df["publish_date"].astype(str),
#         trend_df["video_count"],
#         marker="o",
#         color="#22c55e"
#     )
#     ax2.set_ylabel("Videos")
#     st.pyplot(fig2, use_container_width=True)

