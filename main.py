import visualize_data as VISUALIZE
import collect_data as COLLECT
import calculate_stats as STATS
import download_video as DOWNLOAD


def select():
    print("-" * 20)
    print("Choose an option:")
    print("1. Get data from a channel")
    print("2. Visualize data")
    print("3. Get channel statistics")
    print("4. Download videos")
    print("5. Exit")
    print("-" * 20)
    inp = input("Option: ")
    option = int(inp) if inp.isdigit() else 0
    if option == 1:
        COLLECT.main()
    elif option == 2:
        VISUALIZE.main()
    elif option == 3:
        STATS.main()
    elif option == 4:
        DOWNLOAD.main()
    elif option == 5:
        exit()


def main():
    while True:
        select()


if __name__ == "__main__":
    main()
