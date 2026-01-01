@echo off
REM Void Dominion Launcher for Windows
REM Double-click this file to run the game

echo ================================================
echo        SPACE FRONTIER - USB Edition
echo ================================================
echo.
echo Starting game...
echo.

REM Try python first, then python3
python gui.py 2>NUL
if %ERRORLEVEL% NEQ 0 (
    python3 gui.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Python not found!
    echo.
    echo Please install Python 3.10 or higher from:
    echo https://www.python.org/downloads/
    echo.
    pause
)
