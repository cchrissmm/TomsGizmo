import os
import random
import tkinter as tk
import vlc
from tkinter import messagebox, filedialog
from pynput import keyboard

# Create a VLC player
player = vlc.MediaPlayer()

def select_folder():
    """Opens a directory selection dialog and sets the selected directory as the folder path."""
    global folder_path

    # Open the directory selection dialog
    folder_path = filedialog.askdirectory()

    # Check if a directory was selected
    if not folder_path:
        messagebox.showinfo("Info", "No folder selected.")
    else:
        messagebox.showinfo("Info", f"Selected folder: {folder_path}")

        # Save the selected folder path to a file
        with open("folder_path.txt", "w") as file:
            file.write(folder_path)

# Global variable to keep track of the current index
current_index = 0

def choose_and_play_file():
    """Stops current playback, chooses the next file, and plays it."""
    global player
    global current_index

    # Stop current playback if it's happening
    if player.is_playing():
        player.stop()

    try:
        # Load the folder path from a file
        with open("folder_path.txt", "r") as file:
            folder_path = file.read()
    except FileNotFoundError:
        folder_path = ""

    # If the folder path is empty, open the select folder dialog
    if not folder_path:
        select_folder()

    try:
        # Get a list of files from the folder
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            messagebox.showinfo("Info", "No files found in the folder.")
            return

        # Get the next file
        selected_file = files[current_index]
        file_path = os.path.join(folder_path, selected_file)

        # Play the selected file
        media = vlc.Media(file_path)
        player.set_media(media)
        player.play()
        player.set_fullscreen(True)

        # Increment the current index, and loop back to 0 if it's at the end of the list
        current_index = (current_index + 1) % len(files)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

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
root.geometry('200x200')  # Window size
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