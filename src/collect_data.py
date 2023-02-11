import os.path
import sys

import requests
import json as JSON

from src.channel import Channel
from src.video import Video
from src import utils

from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("API_KEY", "")

if not os.path.exists("data"):
    os.mkdir("data")


def get_user_id_by_video_url():
    video_url = input("Enter video url: ")
    if "youtu.be" in video_url:
        video_id = video_url.split("/")[-1]
    elif "youtube.com" in video_url:
        video_id = video_url.split("v=")[-1]
    else:
        print("Invalid url")
        sys.exit()

    video_response = requests.get("https://www.googleapis.com/youtube/v3/videos", params={
        "part": "snippet",
        "id": video_id,
        "key": KEY,
    })
    if video_response.status_code != 200:
        print("Error while getting video")
        print(video_response.text)
        sys.exit()
    json = video_response.json()
    if json["pageInfo"]["totalResults"] == 0:
        print("No video found")
        sys.exit()

    user_id = json["items"][0]["snippet"]["channelId"]
    return user_id


def get_channel(user_id):
    channelResponse = requests.get("https://www.googleapis.com/youtube/v3/channels", params={
        "part": "contentDetails, statistics, snippet",
        "id": user_id,
        "key": KEY,
    })

    if channelResponse.json()["pageInfo"]["totalResults"] == 0:
        print("No channel found")
        sys.exit()

    channel = channelResponse.json()["items"][0]
    uploads_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
    name = channel["snippet"]["title"]
    view_count = channel["statistics"]["viewCount"]
    subscriber_count = channel["statistics"]["subscriberCount"] if "subscriberCount" in channel["statistics"] else -1
    video_count = channel["statistics"]["videoCount"]
    return Channel(name=name,
                   video_count=video_count,
                   upload_playlist_id=uploads_id,
                   view_count=view_count,
                   channel_id=user_id,
                   subscriber_count=subscriber_count)


def get_videos_from_response(playlist_response, video_response):
    videos = []
    for item in playlist_response.json()["items"]:
        title = item["snippet"]["title"]
        url = "https://www.youtube.com/watch?v=" + item["snippet"]["resourceId"]["videoId"]
        date = item["snippet"]["publishedAt"].split("T")[0]
        time = item["snippet"]["publishedAt"].split("T")[1].split("Z")[0]
        videos.append(Video(title, url, date, time))

    for index, item in enumerate(video_response.json()["items"]):
        view_count = item["statistics"]["viewCount"]
        like_count = item["statistics"]["likeCount"] if "likeCount" in item["statistics"] else 0
        comment_count = item["statistics"]["commentCount"] if "commentCount" in item["statistics"] else 0
        duration = item["contentDetails"]["duration"]
        videos[index].set(view_count, like_count, comment_count, duration)
    return videos


def get_videos(playlist_id):
    playlist_id = playlist_id
    playlist_response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params={
        "part": "snippet",
        "playlistId": playlist_id,
        "key": KEY,
        "maxResults": 50,
    })

    totalResults = playlist_response.json()["pageInfo"]["totalResults"]
    resultsPerPage = playlist_response.json()["pageInfo"]["resultsPerPage"]

    videos = []
    for item in range(0, totalResults, resultsPerPage):
        print(
            f"Getting videos {item + 1} to {item + resultsPerPage if item + resultsPerPage < totalResults else totalResults} of {totalResults}")
        params = {
            "part": "snippet",
            "playlistId": playlist_id,
            "key": KEY,
            "maxResults": 50,
        }
        if "nextPageToken" in playlist_response.json():
            params["pageToken"] = playlist_response.json()["nextPageToken"]

        playlist_response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params=params)
        video_response = requests.get("https://www.googleapis.com/youtube/v3/videos", params={
            "part": "statistics, contentDetails",
            "id": ",".join([item["snippet"]["resourceId"]["videoId"] for item in playlist_response.json()["items"]]),
            "key": KEY,
        })
        videos += get_videos_from_response(playlist_response, video_response)

    return videos


def main():
    user_id = get_user_id_by_video_url()
    channel = get_channel(user_id)
    username = channel.name
    print(f"Getting channel {username} ({channel.channel_id})")

    pretty = True
    videos = get_videos(channel.upload_playlist_id)
    channel.set_videos(videos)

    # remove all symbols from username
    filename = utils.remove_symbols(username)

    with open(f"data/{filename}.json", "w", encoding="utf-8") as f:
        f.write(JSON.dumps(channel.to_json(), indent=4 if pretty else None, ensure_ascii=False))


if __name__ == "__main__":
    main()
