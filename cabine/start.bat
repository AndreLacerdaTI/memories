@echo off
start msedge --start-fullscreen http://127.0.0.1:5000
python fullscreen.py
python app.py
exit