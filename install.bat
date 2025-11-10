@echo off
REM Void Dominion - Windows Installation Script
REM Run this ONCE on each new computer to install dependencies

echo ========================================
echo  VOID DOMINION - INSTALLATION WIZARD
echo ========================================
echo.

REM Change to the directory where this batch file is located
cd /d %~dp0

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.6 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check the box that says
    echo "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not installed
    echo Please reinstall Python and ensure pip is included
    echo.
    pause
    exit /b 1
)

echo pip found!
echo.
echo Installing game dependencies...
echo This may take a minute...
echo.

REM Install requirements
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo     INSTALLATION COMPLETE!
echo ========================================
echo.
echo You can now play Void Dominion!
echo.
echo To start the game:
echo   - Double-click "play.bat"
echo   - Or run: python launch.py
echo.
echo Your game saves will be stored in this folder
echo and will travel with your USB drive.
echo.
echo Enjoy your space adventures, Commander!
echo ========================================
echo.
pause
