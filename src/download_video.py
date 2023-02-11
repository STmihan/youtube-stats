import os
import pytube as Pytube

import src.get as GET
from src import utils

if not os.path.exists("output"):
    os.mkdir("output")


def _download_video(video, path, filename):
    try:
        url = Pytube.YouTube(video.url, on_progress_callback=utils.on_progress)
        streams = [stream for stream in url.streams if stream.resolution is not None]
        streams = list(sorted(streams, key=utils.sort_by_resolution, reverse=True))
        yt_video = streams[0]
        print(f"Resolution: for '{video.title}' is {yt_video.resolution}")
        yt_video.download(output_path=path, filename=filename)
    except Exception as e:
        print(e)
        return False
    return True


def _start_download(videos, username):
    print("-" * 50)
    output_folder = os.path.join("output", username)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    for video in videos:
        filename = f"{utils.remove_symbols(video.title)}.mp4"
        path = os.path.join(output_folder, filename)
        if os.path.exists(path):
            print(f"Video '{video.title}' already exists in '{path}'")
            print(f"Skipping")
            print("-" * 50)
            continue

        print(f"Downloading '{video.title}'")
        result = _download_video(video, path=output_folder, filename=filename)
        if result:
            print(f"\nDownloaded '{video.title}' to '{path}'")
        else:
            print(f"Failed to download '{video.title}'")
            continue
        print("Downloaded {}/{}".format(videos.index(video) + 1, len(videos)))
        print("-" * 50)


def main():
    bundle = GET.get_videos()
    videos = bundle["videos"]
    name = bundle["name"]
    print(f"Found {len(videos)} videos for '{name}'")
    confirm = input("Do you want to download these videos? (Y/n): ").lower() != "n"
    if confirm:
        _start_download(videos, name)


if __name__ == "__main__":
    main()
