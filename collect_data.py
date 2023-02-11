import os.path

from dotenv import load_dotenv
import requests
import json as JSON
import utils as Utils

from video import Video

load_dotenv()

KEY = os.getenv("API_KEY", "")
if not os.path.exists("data"):
    os.mkdir("data")


def get_user_nickname(user_id):
    user_response = requests.get("https://www.googleapis.com/youtube/v3/channels", params={
        "part": "snippet",
        "id": user_id,
        "key": KEY,
    })
    json = user_response.json()
    if json["pageInfo"]["totalResults"] == 0:
        print("No user found")
        exit()

    nickname = json["items"][0]["snippet"]["title"]
    print(f"Found nickname: {nickname}")
    return nickname


def get_user_id_by_video_url():
    video_url = input("Enter video url: ")
    if "youtu.be" in video_url:
        video_id = video_url.split("/")[-1]
    elif "youtube.com" in video_url:
        video_id = video_url.split("v=")[-1]
    else:
        print("Invalid url")
        exit()

    video_response = requests.get("https://www.googleapis.com/youtube/v3/videos", params={
        "part": "snippet",
        "id": video_id,
        "key": KEY,
    })
    json = video_response.json()
    if json["pageInfo"]["totalResults"] == 0:
        print("No video found")
        exit()

    user_id = json["items"][0]["snippet"]["channelId"]
    print(f"Found user id: {user_id}")
    return user_id


def get_playlist_id(user_id):
    channelResponse = requests.get("https://www.googleapis.com/youtube/v3/channels", params={
        "part": "contentDetails",
        "id": user_id,
        "key": KEY,
    })

    if channelResponse.json()["pageInfo"]["totalResults"] == 0:
        print("No channel found")
        exit()

    uploads_id = channelResponse.json()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    print(f"Found uploads playlist: {uploads_id}")
    return uploads_id


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


def get_videos(user_id):
    playlist_id = get_playlist_id(user_id)
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
    username = get_user_nickname(user_id)

    pretty = True
    videos = get_videos(user_id)

    # remove all symbols from username
    filename = Utils.remove_symbols(username)

    with open(f"data/{filename}.json", "w", encoding="utf-8") as f:
        f.write(JSON.dumps([video.to_json() for video in videos], indent=(4 if pretty else None), ensure_ascii=False))


if __name__ == "__main__":
    main()
