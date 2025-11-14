@echo off
REM Quick script to create a versioned release for Windows

SET VERSION=2.0.0
SET RELEASE_NAME=Space-Frontier-v%VERSION%

REM Create release directory
if not exist releases mkdir releases
if not exist releases\%RELEASE_NAME% mkdir releases\%RELEASE_NAME%

REM Copy all necessary files
copy *.py releases\%RELEASE_NAME%\
copy *.md releases\%RELEASE_NAME%\
copy *.txt releases\%RELEASE_NAME%\
copy *.bat releases\%RELEASE_NAME%\
copy *.sh releases\%RELEASE_NAME%\

echo Release directory created: releases\%RELEASE_NAME%
echo.
echo To create ZIP:
echo 1. Right-click the folder: releases\%RELEASE_NAME%
echo 2. Select "Send to" - "Compressed (zipped) folder"
echo 3. Upload to GitHub releases
echo.
echo Or use PowerShell:
echo Compress-Archive -Path releases\%RELEASE_NAME% -DestinationPath releases\%RELEASE_NAME%.zip
pause
