from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import tkinter as tk
from tkinter import messagebox, scrolledtext
from pynput import keyboard

def show_network_error_dialog():
    """Shows a dialog box for network errors with retry and exit options."""
    root.deiconify()
    response = messagebox.askretrycancel("Network Error", "Check your internet connection.")
    if response:
        open_next_link()
    else:
        driver.quit()
        root.quit()

def update_gui_log(message):
    """Updates the GUI with the provided message."""
    log_text.configure(state='normal')
    log_text.insert(tk.END, message + "\n")
    log_text.configure(state='disabled')
    log_text.see(tk.END)

def open_next_link():
    """Opens the next link from the file and handles various errors."""
    global current_link_index, driver
    try:
        with open("links.txt", "r") as file:
            links = file.readlines()
            if not links:
                update_gui_log("The links file is empty.")
                return

            if current_link_index >= len(links):
                current_link_index = 0

            url = links[current_link_index].strip()
            if not url:
                update_gui_log("Encountered an empty URL in the list.")
                current_link_index += 1
                if current_link_index < len(links):
                    open_next_link()
                return
            
            # Display the URL in the text box
            update_gui_log("Trying to play: " + url)

            driver.get(url)

            # Maximize the browser window
            driver.maximize_window()
            # Wait for the page to load and then play the video
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
            driver.execute_script("document.querySelector('video').play();")
            # Wait for the fullscreen button to become clickable
            fullscreen_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.ytp-fullscreen-button.ytp-button')))
            # Click the fullscreen button
            fullscreen_button.click()
            current_link_index += 1

    except (FileNotFoundError, IOError) as e:
        update_gui_log(f"File error: {e}")
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        update_gui_log(f"Error with the link: {e}. Moving to next link.")
        current_link_index += 1
        if current_link_index < len(links):
            open_next_link()
    except Exception as e:
        update_gui_log(f"An unexpected error occurred: {e}. Showing network error dialog.")
        show_network_error_dialog()

def on_press(key):
    """Handles keyboard press events."""
    if str(key) == "'b'":
        open_next_link()

# Firefox options to enable autoplay
firefox_options = Options()
firefox_options.set_preference("media.autoplay.default", 0)
firefox_options.set_preference("media.autoplay.enabled.user-gestures-needed", False)
firefox_options.set_preference("media.autoplay.block-webaudio", False)

# Initialize browser driver
driver = webdriver.Firefox(options=firefox_options)
driver.fullscreen_window()

current_link_index = 0

# Setup the GUI
root = tk.Tk()
root.title("YouTube Player")
root.geometry('400x400')  # Window size

# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

open_link_button = tk.Button(button_frame, text="Play Next Video", command=open_next_link)
open_link_button.pack(side=tk.LEFT, padx=10)

# Add a quit button
quit_button = tk.Button(button_frame, text="Quit", command=root.quit)
quit_button.pack(side=tk.LEFT, padx=10)

log_text = scrolledtext.ScrolledText(root, state='disabled', height=10)
log_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Listener for button press
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Start the GUI event loop
root.mainloop()

# Cleanup
listener.stop()
driver.quit()
