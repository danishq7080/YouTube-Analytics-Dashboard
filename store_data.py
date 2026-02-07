from youtube_api import get_channel_details, get_video_ids, get_video_details
from database import create_tables, insert_channel, insert_videos

CHANNEL_ID = "UC_x5XG1OV2P6uZZ5FSM9Ttw"

def main():
    create_tables()

    channel = get_channel_details(CHANNEL_ID)
    insert_channel(channel)

    video_ids = get_video_ids(CHANNEL_ID)
    videos_df = get_video_details(video_ids)
    insert_videos(videos_df, CHANNEL_ID)

    print("Data stored successfully!")

if __name__ == "__main__":
    main()
