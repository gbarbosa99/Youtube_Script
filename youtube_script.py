import csv
import json

import requests

api_url = 'https://www.googleapis.com/youtube/v3/search?channelId=UCJFp8uSYCjXOMnkUyb3CQ3Q&part=snippet&key=AIzaSyD6QQJ4EViRRdT7y89l3xaeZczNviMbp1k'

api_response = requests.get(api_url)
videos = json.loads(api_response.text)

with open("youtube_videos.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["publishedAt",
                         "title",
                         "description",
                         "thumbnails"])
    has_another_page = True
    while has_another_page:
        if videos.get('items') is not None:
            for video in videos.get('items'):
                video_data_row = [
                    video['snippet']['publishedAt'],
                    video['snippet']['title'].encode('utf-8'),
                    video['snippet']['description'].encode('utf-8'),
                    video['snippet']['thumbnails']['default']['url'].encode('utf-8')
                    ]
                csv_writer.writerow(video_data_row)
        if 'nextPageToken' in videos.keys():
            next_page_url = api_url + '&pageToken=' + videos['nextPageToken']
            next_page_posts = requests.get(next_page_url)
            videos = json.loads(next_page_posts.text)
        else:
            print("no more videos!")
            has_another_page = False
