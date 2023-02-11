import pytube as Pytube

import src.utils as Utils


def _download_one(url):
    yt_video = Pytube.YouTube(url, on_progress_callback=Utils.on_progress)
    author = yt_video.author.title()
    author = Utils.remove_symbols(author)
    streams = yt_video.streams
    streams = [stream for stream in streams if stream.resolution is not None]
    streams = list(sorted(streams, key=Utils.sort_by_resolution, reverse=True))
    for i in range(len(streams)):
        print(f"{i}. {streams[i].resolution}")
    inp = input("Choose a resolution: ")
    if not inp.isdigit():
        print("Invalid input")
        return
    index = int(inp)
    if index < 0 or index >= len(streams):
        print("Invalid input")
        return
    stream = streams[index]
    print(f"Downloading {stream.title}...")
    filename = f"{Utils.remove_symbols(stream.title)}.mp4"
    stream.download(output_path=f"output/{author}", filename=filename)


def main():
    print("-" * 50)
    url = input("Enter a video URL: ")
    if not url:
        print("Invalid URL")
        return
    yt_video = Pytube.YouTube(url)
    if not yt_video.title:
        print("Invalid URL")
        return
    _download_one(url)
    print("Done downloading video " + yt_video.title)
