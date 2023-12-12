import tkinter as tk
import subprocess
import os

def open_next_link():
    global current_link_index
    vlc_path = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"  # Update this line

    try:
        with open("links.txt", "r") as file:
            links = file.readlines()
            if not links:
                print("The links file is empty.")
                return

            url = links[current_link_index].strip()
            print(f"Opening link: {url}")

            try:
                # Reduced caching time for quicker start
                subprocess.Popen([vlc_path, "--network-caching=300", "--one-instance", "--play-and-exit", url])
            except Exception as e:
                print("Error opening VLC:", e)

            current_link_index = (current_link_index + 1) % len(links)

    except FileNotFoundError:
        print("The links file was not found.")

current_link_index = 0

root = tk.Tk()
root.title("Link Opener in VLC")

open_link_button = tk.Button(root, text="Open Next Link in VLC", command=open_next_link)
open_link_button.pack(pady=20)

root.mainloop()
