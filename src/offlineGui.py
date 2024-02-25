#!/usr/bin/env python3
import os
import tkinter as tk
import vlc
from tkinter import messagebox, filedialog
from pynput import keyboard
import psutil
import logging
import time

last_key_press_time = {'b': 0, 'q': 0}
debounce_time = 2  # in seconds

# Configure logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# Global variable to keep track of the current index
current_index = 0
player = vlc.MediaPlayer()

def get_removable_media_paths():
    """Returns a list of mount points for all removable media currently inserted."""
    removable_media_paths = []
    base_path = '/media'
    if os.path.exists(base_path):
        for user_dir in os.listdir(base_path):
            user_path = os.path.join(base_path, user_dir)
            if os.path.isdir(user_path):
                for dir_name in os.listdir(user_path):
                    full_path = os.path.join(user_path, dir_name)
                    if os.path.isdir(full_path):
                        removable_media_paths.append(full_path)
    return removable_media_paths

def stop():
# Stop current playback 
    player.stop()

def resume():
    player.resume()

def choose_and_play_file():
    """Stops current playback, chooses the next file from removable media, and plays it."""
    global player
    global current_index

    # Stop current playback if it's happening
    if player.is_playing():
        player.stop()

    # Get the paths of all removable media
    removable_media_paths = get_removable_media_paths()
    if not removable_media_paths:
        messagebox.showinfo("Info", "No removable media found.")
        return

    # Get a list of video files from the removable media
    video_files = []
    for path in removable_media_paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(('.mp4', '.mkv', '.avi')):  # Add more video file extensions if needed
                    video_files.append(os.path.join(root, file))

    if not video_files:
        messagebox.showinfo("Info", "No video files found on the removable media.")
        return

    # Get the next video file
    selected_file = video_files[current_index]
    file_path = selected_file

    # Play the selected file
    media = vlc.Media(file_path)
    player.set_media(media)
    player.play()
    time.sleep(1)
    player.set_fullscreen(True)

    # Increment the current index, and loop back to 0 if it's at the end of the list
    current_index = (current_index + 1) % len(video_files)



def on_press(key):
    """Handles key press events."""
    global last_key_press_time
    try:
        current_time = time.time()
        if key.char == 'b': 
            if current_time - last_key_press_time['b'] > debounce_time:
                choose_and_play_file()
            last_key_press_time['b'] = current_time
        if key.char == 'q':
            if current_time - last_key_press_time['q'] > debounce_time:
                root.quit()
            last_key_press_time['q'] = current_time 
        if key.char == 'r':
            resume()   
    except AttributeError:
        pass

# Setup the GUI
root = tk.Tk()
root.title("Play")
root.attributes('-fullscreen', True)  # Make the Tkinter window fullscreen

# Create a Frame and pack it
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=1)

# Create a Canvas and pack it
canvas = tk.Canvas(frame)
canvas.pack(fill=tk.BOTH, expand=1)

# Embed the VLC player in the Canvas
player.set_xwindow(canvas.winfo_id())

# Create a Frame for the buttons and pack it at the bottom
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Create the buttons and pack them on either side of the center
play_button = tk.Button(button_frame, text="Play", command=choose_and_play_file,font=('Helvetica', '16'), width=20)
play_button.pack(side=tk.LEFT, expand=True)

stop_button = tk.Button(button_frame, text="Stop", command=stop, font=('Helvetica', '16'), width=20)
stop_button.pack(side=tk.RIGHT, expand=True)

# Create a Label and pack it to the left
label = tk.Label(button_frame, text="Tom's Gizmo", font=('Helvetica', '16'))
label.pack(side=tk.LEFT)

# Configure logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# Use logging in your application
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')

#quit_button = tk.Button(root, text="Quit", command=root.quit)
#quit_button.pack(pady=5)

# Start the key listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Start the GUI event loop
root.mainloop()