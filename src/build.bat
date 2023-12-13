@echo off

REM Change to your Python script's name
SET PYTHON_SCRIPT=gui.py

REM Path to geckodriver.exe
SET GECKODRIVER_PATH=geckodriver.exe  

REM Path to links.txt
SET LINKS_TXT_PATH=links.txt

REM Building the executable
pyinstaller --onefile --windowed %PYTHON_SCRIPT%

REM Copy geckodriver.exe and links.txt to the dist folder
copy "%GECKODRIVER_PATH%" .\dist\
copy "%LINKS_TXT_PATH%" .\dist\

echo Build and copy process completed.
pause