#!/usr/bin/env python3
import os
# Set the current working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import logging
logging.basicConfig(filename='logfile.log', level=logging.DEBUG)
logging.debug('This message will be written to the log file.')


import subprocess
import sys
def install_packages():
    """Install required packages."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
try:
    import pyautogui
    from pynput import mouse
except ImportError:
    install_packages()
    # Now, after installing, import again
    import pyautogui
    from pynput import mouse

import pyautogui
import time
import random
import argparse
from pynput import mouse
import tkinter as tk
from tkinter import simpledialog, messagebox


running = True

def on_click(x, y, button, pressed):
    """Callback for mouse click events."""
    global running
    # If the button is released and it's the left button, check for double click
    if not pressed and button == mouse.Button.left:
        if hasattr(on_click, "click_time"):
            # If the time between two releases of the left button is less than 0.5 seconds, stop the program
            if time.time() - on_click.click_time < 0.5:
                running = False
        on_click.click_time = time.time()

def move_mouse_randomly(duration=1, max_time=30):
    """Move mouse to a random position on the screen for a maximum duration.
    
    - duration (float): The duration in second to take for each move.
    - max_time (int): The maximum time in min to keep moving the mouse.
    """
    end_time = time.time() + max_time*60
    while running and time.time() < end_time:
        screenWidth, screenHeight = pyautogui.size()
        
        x, y = random.randint(0, screenWidth-1), random.randint(0, screenHeight-1)
        pyautogui.moveTo(x, y, duration=duration)
        time.sleep(duration)  # Wait for the specified duration before the next move

def start_movement():
    global running
    duration = float(duration_entry.get())
    max_time = int(max_time_entry.get())
    
    running = True
    
    # Start a mouse listener in a separate thread
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    
    move_mouse_randomly(duration, max_time)
    
    listener.stop()

# if __name__ == "__main__":
#     time.sleep(5)  # Sleep for 5 seconds before starting
    
#     parser = argparse.ArgumentParser(description='Move mouse randomly for a specified time.')
#     parser.add_argument('--duration', type=float, default=0.5, help='Duration in second for moves.')
#     parser.add_argument('--max_time', type=int, default=30, help='Maximum time in minutes to move the mouse.')
#     args = parser.parse_args()
    
#     # Start a mouse listener in a separate thread
#     listener = mouse.Listener(on_click=on_click)
#     listener.start()
    
#     move_mouse_randomly(args.duration, args.max_time)
    
#     listener.stop()
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Mouse Mover")
    
    tk.Label(root, text="Duration (seconds):").pack(pady=10)
    duration_entry = tk.Entry(root)
    duration_entry.insert(0, "0.5")
    duration_entry.pack(pady=5)

    tk.Label(root, text="Max Time (minutes):").pack(pady=10)
    max_time_entry = tk.Entry(root)
    max_time_entry.insert(0, "30")
    max_time_entry.pack(pady=5)
    max_time_entry.bind("<Return>", lambda event=None: start_movement())  # Bind Enter key
    
    start_button = tk.Button(root, text="Start Movement", command=start_movement)
    start_button.pack(pady=20)
    
    root.mainloop()