from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pynput import keyboard
import tkinter as tk
import threading

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def open_next_link():
    global current_link_index, driver
    try:
        with open("links.txt", "r") as file:
            links = file.readlines()
            if not links:
                print("The links file is empty.")
                return

            if current_link_index >= len(links):
                current_link_index = 0  # Loop back to the start

            url = links[current_link_index].strip()

            # Open the link in the browser
            driver.get(url)

            # Wait for the video to load
            wait = WebDriverWait(driver, 10)
            video = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'video')))

            # Play the video
            video.click()

            # Wait for the fullscreen button to become clickable
            fullscreen_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.ytp-fullscreen-button.ytp-button')))

            # Click the fullscreen button
            fullscreen_button.click()


            # Increment the index for the next link
            current_link_index += 1

    except FileNotFoundError:
        print("The links file was not found.")

def on_press(key):
    if str(key) == "'b'":
        open_next_link()

# Set Firefox options to enable autoplay
firefox_options = Options()
firefox_options.set_preference("media.autoplay.default", 0)  # 0 means "Allow all", 1 means "Block all"
firefox_options.set_preference("media.autoplay.enabled.user-gestures-needed", False)
firefox_options.set_preference("media.autoplay.block-webaudio", False)

# Initialize the browser driver with the custom options
driver = webdriver.Firefox(options=firefox_options)

# Open the browser in fullscreen mode
driver.fullscreen_window()

current_link_index = 0

# Setup the GUI
root = tk.Tk()
root.title("YouTube Player")

open_link_button = tk.Button(root, text="Play Next Video", command=open_next_link)
open_link_button.pack(pady=20)

# Start the listener for the button press in a separate thread
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Start the GUI event loop
root.mainloop()

# Clean up
listener.stop()
driver.quit()
