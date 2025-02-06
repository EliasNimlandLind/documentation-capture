import time
import os
import threading
import math
import configparser

import pygetwindow as pygetwindow
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key
from PIL import  ImageDraw, Image, ImageGrab

from draw import draw_arrow, draw_text_box, draw_new_screenshot

from math_helper import get_arrow_direction

# Read configuration file
config_parser = configparser.ConfigParser()
config_parser.read('config.ini')
base_directory = config_parser.get("directories", "output").replace('%Y-%m-%d', time.strftime('%Y-%m-%d'))

print(base_directory)
output_directory = base_directory
counter = 1

while os.path.exists(output_directory):
    output_directory = f"{base_directory}_{counter}"
    counter += 1

os.makedirs(output_directory, exist_ok=True)

terminate_event = threading.Event()
current_step = 1

arrow_length = config_parser.get("arrow","length")
arrow_width = config_parser.get("arrow","width")

def on_click(mouse_x, mouse_y, button, pressed):
    global current_step
    if terminate_event.is_set():
        return False  # Stop the mouse listener

    if pressed:
        active_window = pygetwindow.getActiveWindow()
        if active_window:
            window_box = active_window.left, active_window.top, active_window.right, active_window.bottom
        else:
            print("No active window found.")
            return

        # Capture screenshot of the active window
        draw_new_screenshot(window_box)
        screenshot = ImageGrab.grab(bbox=window_box)
        
        width, height = screenshot.size
        new_height = height + config_parser.getint("text_box", "height")
        new_screenshot = Image.new("RGB", (width, new_height), (255, 255, 255))  # Create new blank image

        new_screenshot.paste(screenshot, (0, 0))

        draw = ImageDraw.Draw(new_screenshot)

        draw_text_box(draw, width, height, new_height)

        screen_width, screen_height = pygetwindow.getWindowsWithTitle(active_window.title)[0].width, pygetwindow.getWindowsWithTitle(active_window.title)[0].height
        
        arrow_angle = get_arrow_direction((mouse_x, mouse_y), screen_width, screen_height)

        end_x = mouse_x + 40 * math.cos(arrow_angle)
        end_y = mouse_y + 40 * math.sin(arrow_angle)
        
        draw_arrow(draw, (mouse_x, mouse_y), (end_x, end_y))

        new_screenshot.save(f"{output_directory}/step-{current_step}.png")
        print("Saved screenshot to " + f"{output_directory}/step-{current_step}.png")
        current_step += 1

def on_press(key):
    if key == Key.esc:
        print("Terminating all processes...")
        terminate_event.set()
        return False  # Stops the keyboard listener

def start_listening():
    with MouseListener(on_click=on_click) as mouse_listener:
        while not terminate_event.is_set():
            time.sleep(0.1)  # Avoid high CPU usage
        mouse_listener.stop()

def start_keyboard_listener():
    with KeyboardListener(on_press=on_press) as keyboard_listener:
        keyboard_listener.join()

def main():
    # Run listeners in separate threads
    listener_thread = threading.Thread(target=start_listening)
    keyboard_thread = threading.Thread(target=start_keyboard_listener)

    listener_thread.start()
    keyboard_thread.start()

    listener_thread.join()
    keyboard_thread.join()

if __name__ == "__main__":
    main()