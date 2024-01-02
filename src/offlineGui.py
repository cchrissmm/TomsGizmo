import os
import random
import tkinter as tk
import vlc
from tkinter import messagebox
from pynput import keyboard

def on_press(key):
    """Handles key press events."""
    # Check if the 'b' key was pressed
    if key == keyboard.KeyCode.from_char('b'):
        choose_and_play_file()

# Listener for button press
listener = keyboard.Listener(on_press=on_press)
listener.start()

def choose_and_play_file():
    """Stops current playback, chooses a random file, and plays it."""
    global player

    # Stop current playback if it's happening
    if player.is_playing():
        player.stop()

    try:
        # Choose a random file from the folder
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            messagebox.showinfo("Info", "No files found in the folder.")
            return

        selected_file = random.choice(files)
        file_path = os.path.join(folder_path, selected_file)

        # Play the selected file
        media = vlc.Media(file_path)
        player.set_media(media)
        player.play()
        player.set_fullscreen(True)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def on_quit():
    """Cleanup function to call before quitting."""
    listener.stop()
    player.stop()
    root.quit()

# Set the folder path
folder_path = "C:\\Users\\cchri\\OneDrive\\Desktop\\YouTubeDownloads"

# Initialize VLC player
player = vlc.MediaPlayer()

# Setup the GUI
root = tk.Tk()
root.title("Random File Player")
root.geometry('400x200')  # Window size

play_button = tk.Button(root, text="Play Random File", command=choose_and_play_file)
play_button.pack(pady=20)

quit_button = tk.Button(root, text="Quit", command=on_quit)
quit_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
