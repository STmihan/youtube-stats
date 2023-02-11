import datetime as DT
import json as JSON
import os

from video import Video

FROM_DATE = DT.date(year=2000, month=1, day=1)
TO_DATE = DT.date.today()
INCLUDE_SHORT_VIDEOS = False


def _get_videos_data(path):
    with open(path, "r", encoding="utf-8") as f:
        videos_json = JSON.load(f)
        videos = []
        for json in videos_json:
            video = Video.from_json(json)
            videos.append(video)

        return videos


def _get_video_between_dates(videos, date_from, date_to):
    videos_between_dates = []
    for video in videos:
        date_split = video.date.split("-")
        date = DT.date.fromisoformat(f"{date_split[0]}-{date_split[1]}-{date_split[2]}")
        if date_from <= date <= date_to:
            videos_between_dates.append(video)
    return videos_between_dates


def print_files(dir):
    print("-" * 20)
    files = dir
    for i, file in enumerate(files):
        name = file.replace(".json", "")
        print(f"{i}: {name}")
    print("-" * 20)


def _select_path():
    files = os.listdir("data")
    print_files(files)
    index = int(input("Select a file: "))
    return f"data/{files[index]}"


def _select_options():
    global INCLUDE_SHORT_VIDEOS, FROM_DATE, TO_DATE
    include_short_videos = input("Include short videos? (y/N): ") == "y"
    INCLUDE_SHORT_VIDEOS = include_short_videos if include_short_videos else INCLUDE_SHORT_VIDEOS
    from_date = input("From date (YYYY-MM-DD) (default: 2000-01-01): ")
    FROM_DATE = DT.date.fromisoformat(from_date) if from_date else FROM_DATE
    to_date = input("To date (YYYY-MM-DD) (default: today): ")
    TO_DATE = DT.date.fromisoformat(to_date) if to_date else TO_DATE


def get_videos():
    path = _select_path()
    name = path.split("/")[-1].split(".")[0]
    _select_options()

    videos = _get_videos_data(path)
    videos = [video for video in videos if not video.is_short] if not INCLUDE_SHORT_VIDEOS else videos
    videos = _get_video_between_dates(videos, FROM_DATE, TO_DATE)
    return {
        "name": name,
        "videos": videos,
    }


def get_multiple_videos():
    _select_options()
    bundles = []
    files = os.listdir("data")
    print_files(files)
    numbers = input("Select files (separated by space): ").split(" ")

    for number in numbers:
        path = f"data/{os.listdir('data')[int(number)]}"
        name = path.split("/")[-1].split(".")[0]
        videos_data = _get_videos_data(path)
        videos_data = [video for video in videos_data if
                       not video.is_short] if not INCLUDE_SHORT_VIDEOS else videos_data
        videos_data = _get_video_between_dates(videos_data, FROM_DATE, TO_DATE)
        bundles.append({
            "name": name,
            "videos": videos_data,
        })

    return bundles
