@echo off
SET SCRIPT_NAME=offlineGui.py
SET PYINSTALLER_OPTIONS=

REM Echo the script name and PyInstaller options
echo Building %SCRIPT_NAME% with PyInstaller options: %PYINSTALLER_OPTIONS%

REM Build the Docker image
docker build -t python-app-compiler .

REM Run the Docker container, passing the script name and PyInstaller options
docker run -e SCRIPT_NAME=%SCRIPT_NAME% -e PYINSTALLER_OPTIONS=%PYINSTALLER_OPTIONS% -v %cd%/dist:/app/dist python-app-compiler

echo Compiled file should be in the dist folder
pause
