from youtube_api import get_channel_details, get_video_ids, get_video_details

CHANNEL_ID = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Google Developers

channel = get_channel_details(CHANNEL_ID)
print(channel)

video_ids = get_video_ids(CHANNEL_ID)
videos_df = get_video_details(video_ids)

print(videos_df.head())
