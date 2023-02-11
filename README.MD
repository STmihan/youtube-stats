# YouTube's stats app #

Features:

- Visualize the number of views of a YouTube channel per day, week or month
- Show the average number of views per day, week or month
- Download the data of videos from a YouTube channel (views, likes, comments count, etc.)
- Download videos from a YouTube channel

## Installation ##

### Source code ###

1. Install Python 3.6 or higher
2. Install the required packages: `pip install -r requirements.txt`
3. Run the app: `python main.py` (or `python3 main.py` on Linux)

### Executable ###

1. Download the latest release from the [releases page](https://github.com/STmihan/youtube-stats/releases)
2. Run the app: `youtube-stats.exe` (or `./youtube-stats` on Linux)

## Getting Started ##

### Source code ###
1. Go to the [YouTube Data API v3 page](https://console.developers.google.com/apis/api/youtube.googleapis.com/overview)
   and create a project
2. Enable the YouTube Data API v3 API
3. Create an API key
4. Create a file named '.env' and write to it: ```API_KEY=YOUR_API_KEY # Replace YOUR_API_KEY with your API key```
5. Run the app: `python main.py` (or `python3 main.py` on Linux)
6. Press '1' and enter some YouTube video url from the channel you want to inspect
7. After the download is complete, you can use 2, 3 and 4 to features from the menu
8. Enter 5 to exit the app

### Executable ###
1. After downloading the app from the [releases page](https://github.com/STmihan/youtube-stats/releases), go to the folder where the app is located
2. Run the app from the command line: `youtube-stats.exe` (or `./youtube-stats` on Linux)
3. Press '1' and enter some YouTube video url from the channel you want to inspect
4. After the download is complete, you can use 2, 3 and 4 to features from the menu
5. Enter 5 to exit the app

## Usage ##

### 1. Download all videos from channel ###

1. Enter 1 in the main menu
2. Enter the URL of a video from the channel you want to download
3. After the download is complete, enter 4 in the main menu
4. Choose the channel you want to download
5. Choose, do you want to include short videos (less than 1 minute)
6. Choose start date and end date
7. Confirm the download
8. Videos will be downloaded to the 'output' folder

### 2. Visualize the number of views of a YouTube channel per day, week or month ###

1. Enter 2 in the main menu
2. Enter "n" or just press enter
3. Choose the channel you want to visualize
4. Choose, do you want to include short videos (less than 1 minute)
5. Choose the start date and end date
6. Choose the period you want to visualize 

### 3. Compare the number of views of two YouTube channels per day, week or month ###

1. Enter 2 in the main menu
2. Enter "y"
3. Choose, do you want to use fast mode (will use one filter for all channels)
4. If you chose fast mode, choose the including short videos, start date and end date
5. If you chose fast mode, write the channel numbers you want to compare (separated by spaces)
6. If you didn't choose fast mode, choose the channel you want to compare
7. Choose filter options
8. Choose the period you want to visualize

### 4. Show the channel's statistics ###

1. Enter 3 in the main menu
2. Choose the channel you want to show statistics
3. Choose, do you want to include short videos (less than 1 minute)
4. Choose the start date and end date

### 5. Add a channel to the database ###

1. Enter 1 in the main menu
2. Enter the URL of a video from the channel you want to add
3. After the download is complete, you can use 2, 3 and 4 to features from the menu with new channel

## Build ##
1. Install pyinstaller: `pip install pyinstaller`
2. Install requirements: `pip install -r requirements.txt`
3. Run `python clean.py` (or `python3 clean.py` on Linux)
4. Run the command: `./build.bat` (or `sh build.sh` on Linux)
5. Executable will be in the 'dist' folder