import pyautogui
import time
import random
import argparse
from pynput import mouse


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

if __name__ == "__main__":
    time.sleep(5)  # Sleep for 5 seconds before starting
    
    parser = argparse.ArgumentParser(description='Move mouse randomly for a specified time.')
    parser.add_argument('--duration', type=float, default=0.5, help='Duration in second for moves.')
    parser.add_argument('--max_time', type=int, default=30, help='Maximum time in minutes to move the mouse.')
    args = parser.parse_args()
    
    # Start a mouse listener in a separate thread
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    
    move_mouse_randomly(args.duration, args.max_time)
    
    listener.stop()
