import re


def remove_symbols(string):
    string = "".join([c for c in string if c.isalpha() or c.isdigit() or c == " "]).rstrip()
    string = re.sub(" +", " ", string)
    return string


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"\rDownloaded {percentage:.2f}%", end="")


def sort_by_resolution(stream):
    if stream.resolution is None:
        return 0
    return int(stream.resolution.split("p")[0])