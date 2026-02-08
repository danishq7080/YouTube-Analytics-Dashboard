from analytics import load_data, add_engagement_rate, top_videos, channel_kpis, upload_trend

channels_df, videos_df = load_data()
videos_df = add_engagement_rate(videos_df)

print("Top Videos:")
print(top_videos(videos_df)[["title", "views", "engagement_rate"]])

print("\nChannel KPIs:")
print(channel_kpis(videos_df))

print("\nUpload Trend:")
print(upload_trend(videos_df).head())
