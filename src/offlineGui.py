import os
import tkinter as tk
import vlc
from tkinter import messagebox, filedialog
from pynput import keyboard
import psutil

# Global variable to keep track of the current index
current_index = 0
player = vlc.MediaPlayer()

def get_removable_media_paths():
    """Returns a list of mount points for all removable media currently inserted."""
    removable_media_paths = []
    for partition in psutil.disk_partitions():
        if 'removable' in partition.opts:
            removable_media_paths.append(partition.mountpoint)
    return removable_media_paths

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
    player.set_fullscreen(True)

    # Increment the current index, and loop back to 0 if it's at the end of the list
    current_index = (current_index + 1) % len(video_files)



def on_press(key):
    """Handles key press events."""
    try:
        if key.char == 'b':
            choose_and_play_file()
    except AttributeError:
        pass

# Setup the GUI
root = tk.Tk()
root.title("Play")
root.geometry('200x100+0+0')  # Window size
root.attributes('-topmost', 1)

play_button = tk.Button(root, text="Play File", command=choose_and_play_file)
play_button.pack(pady=5)

select_folder_button = tk.Button(root, text="Select Folder", command=select_folder)
select_folder_button.pack(pady=5)

quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.pack(pady=5)

# Start the key listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Start the GUI event loop
root.mainloop()