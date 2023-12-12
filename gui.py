from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import tkinter as tk

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

            # Increment the index for the next link
            current_link_index += 1

    except FileNotFoundError:
        print("The links file was not found.")

# Set Firefox options to enable autoplay
firefox_options = Options()
firefox_options.set_preference("media.autoplay.default", 0)  # 0 means "Allow all", 1 means "Block all"
firefox_options.set_preference("media.autoplay.enabled.user-gestures-needed", False)
firefox_options.set_preference("media.autoplay.block-webaudio", False)

# Initialize the browser driver with the custom options
driver = webdriver.Firefox(options=firefox_options)

current_link_index = 0

root = tk.Tk()
root.title("YouTube Player")

open_link_button = tk.Button(root, text="Play Next Video", command=open_next_link)
open_link_button.pack(pady=20)

root.mainloop()

# Close the browser when the GUI is closed
driver.quit()
