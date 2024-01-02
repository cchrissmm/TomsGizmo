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

def choose_and_play_file():
    """Stops current playback, chooses a random file, and plays it."""
    global player

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
        # Choose a random file from the folder
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            messagebox.showinfo("Info", "No files found in the folder.")
            return

        # Choose a random file
        selected_file = random.choice(files)
        file_path = os.path.join(folder_path, selected_file)

        # Play the selected file
        media = vlc.Media(file_path)
        player.set_media(media)
        player.play()
        player.set_fullscreen(True)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Setup the GUI
root = tk.Tk()
root.title("Random File Player")
root.geometry('200x200')  # Window size
root.attributes('-topmost', 1)

play_button = tk.Button(root, text="Play Random File", command=choose_and_play_file)
play_button.pack(pady=20)

select_folder_button = tk.Button(root, text="Select Folder", command=select_folder)
select_folder_button.pack(pady=5)

quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()