# Toms Gizmo
Using a program like 4k video downloader, download all the files that you want to view to a usb drive.

Open the program, it will search for removable media like that USB drive and play the songs.

## Install VLC Media player
VLC Needs to be installed first on the target system.

### VLC On Windows
Download and install vlc from the VLC site

### VLC On Linux
sudo apt install python3-vlc
pip install pynput


## Depenedncies
There are a few to install, just run the .py and work out which ones

pip install pynput

## Building for Linux
run this for x86

pyinstaller offlineGui.spec 

run this for arm
pyinstaller offlineGuiArch64.spec 


## Building for Windows
run 

buildOfflineGui.bat








