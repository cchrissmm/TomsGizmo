@echo off

REM Change to your Python script's name
SET PYTHON_SCRIPT=offlineGui.py

REM Building the executable
REM pyinstaller --onefile --windowed %PYTHON_SCRIPT%
pyinstaller --onefile %PYTHON_SCRIPT%

echo Build and copy process completed.
pause