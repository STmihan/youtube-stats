@echo off
pyinstaller --onefile --add-data=".env;.env" --icon=icon.ico --name=youtube_stats main.py