import matplotlib.pyplot as PLT
import matplotlib.ticker as TICKER
import datetime as DT

import get


def _get_compare_type():
    print("-" * 20)
    print("Compare:")
    print("1. Views per day")
    print("2. Views per week")
    print("3. Views per month")
    print("-" * 20)
    option = int(input("Option: "))
    return option


def _compare_by(compare_type, videos):
    if compare_type == 1:
        return _get_view_count_per_day(videos)
    elif compare_type == 2:
        return _get_view_count_per_week(videos)
    elif compare_type == 3:
        return _get_view_count_per_month(videos)


def _get_view_count_per_day(videos):
    view_count_per_day = {}
    for video in videos:
        date = DT.datetime.strptime(video.date, "%Y-%m-%d")
        if date in view_count_per_day:
            view_count_per_day[date] += video.view_count
        else:
            view_count_per_day[date] = video.view_count
    return view_count_per_day


def _get_view_count_per_week(videos):
    view_count_per_week = {}
    for video in videos:
        date = DT.datetime.strptime(video.date, "%Y-%m-%d")
        week = date.isocalendar()[1]
        if week in view_count_per_week:
            view_count_per_week[week] += video.view_count
        else:
            view_count_per_week[week] = video.view_count
    return view_count_per_week


def _get_view_count_per_month(videos):
    view_count_per_month = {}
    for video in videos:
        print(video.view_count)
        date = DT.datetime.strptime(video.date, "%Y-%m-%d")
        month = date.month
        if month in view_count_per_month:
            view_count_per_month[month] += video.view_count
        else:
            view_count_per_month[month] = video.view_count
    return view_count_per_month


def run_visualize(compare_type):
    PLT.title("Compare Views Per " + "Day" if compare_type == 1 else "Week" if compare_type == 2 else "Month")
    PLT.xlabel("Date" if compare_type == 1 else "Week" if compare_type == 2 else "Month")
    PLT.ylabel("View Count")
    PLT.grid()
    PLT.legend()
    PLT.gca().yaxis.set_major_formatter(TICKER.FuncFormatter(lambda x, p: format(int(x), ",")))
    PLT.gcf().set_size_inches(9, 5)
    PLT.show()


def visualize_data(videos, compare_type):
    view_count_per_day = _compare_by(compare_type, videos)
    dates = list(view_count_per_day.keys())
    dates.sort()
    view_counts = [view_count_per_day[date] for date in dates]

    PLT.plot(dates, view_counts, label="View Count")

    run_visualize(compare_type)


def compare_data(video_bundles, compare_type):
    for bundle in video_bundles:
        name = bundle["name"]
        videos = bundle["videos"]
        view_count_per_day = _compare_by(compare_type, videos)
        dates = list(view_count_per_day.keys())
        dates.sort()
        view_counts = [view_count_per_day[date] for date in dates]
        PLT.plot(dates, view_counts, label=name)

    run_visualize(compare_type)


def main():
    compare = input("Compare multiple channels? (y/N): ").lower() == "y"
    if compare:
        fast = input("Fast mode? (Y/n): ").lower() != "n"
        bundles = []
        if fast:
            bundles = get.get_multiple_videos()
        else:
            while True:
                videos = get.get_videos()
                bundles.append(videos)
                if input("Add another channel? (y/N): ").lower() != "y":
                    break
        compare_type = _get_compare_type()
        compare_data(bundles, compare_type)
    else:
        videos = get.get_videos()["videos"]
        compare_type = _get_compare_type()
        visualize_data(videos, compare_type)


if __name__ == "__main__":
    main()
