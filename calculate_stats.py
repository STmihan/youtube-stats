import get_videos


def get_average_views_per_video(videos):
    total_views = 0
    for video in videos:
        total_views += int(video.view_count)
    return round(total_views / len(videos)).__format__(",").replace(",", " ")


def get_average_likes_per_video(videos):
    total_likes = 0
    for video in videos:
        total_likes += int(video.like_count)
    return round(total_likes / len(videos)).__format__(",").replace(",", " ")


def main():
    bundle = get_videos.get_videos()
    videos = bundle["videos"]
    name = bundle["name"]
    print("-" * 20)
    print("Channel: ", name)
    print("Total videos: ", len(videos))
    print("-" * 20)
    print("Average views per video: ", get_average_views_per_video(videos))
    print("Average likes per video: ", get_average_likes_per_video(videos))
    print("-" * 20)


if __name__ == "__main__":
    main()
