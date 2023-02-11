import src.get as get


def main():
    channel = get.get_channel()
    print("-" * 20)
    print(channel)
    print()
    print("Average views per video: ", channel.get_average_views_per_video())
    print("Average likes per video: ", channel.get_average_likes_per_video())


if __name__ == "__main__":
    main()
