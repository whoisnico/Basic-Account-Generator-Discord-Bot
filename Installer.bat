@echo off
REM Check if Python is installed
echo Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    cls
    echo Python is not installed. Please download it from the official website:
    echo https://www.python.org/downloads/windows/
) else (
    echo Installing Disnake...
    REM Install the Disnake package
    python -m pip install disnake
    cls
    echo Disnake has been successfully installed.
    echo Now setup the config.json and start the main.py
)


REM Wait before closing the window
timeout /t 30
