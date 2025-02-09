import time
import os
import threading
import math
import configparser

import pygetwindow as pygetwindow
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key
from PIL import ImageDraw, Image, ImageGrab

from draw import draw_arrow, draw_text_box, draw_new_screenshot, get_color_from_config_parser
from math_helper import get_arrow_direction
from message import print_message

config_parser = configparser.ConfigParser()
config_parser.read('config.ini')
base_directory = config_parser.get("directories", "output").replace('%Y-%m-%d', time.strftime('%Y-%m-%d'))

output_directory = base_directory
counter = 1

while os.path.exists(output_directory):
    output_directory = f"{base_directory}_{counter}"
    counter += 1

os.makedirs(output_directory, exist_ok=True)
print_message("screenshot.outputDirectory", directory=output_directory)

terminate_event = threading.Event()
current_step = 1

arrow_length = config_parser.get("arrow", "length")
arrow_width = config_parser.get("arrow", "width")

secondary_capture_key_as_string = config_parser.get("keybindings", "secondary_screenshot_capture_key")
termination_key_as_string = config_parser.get("keybindings", "termination_key")

control_pressed = False 

def get_key_object(key_as_string):
    key_object = getattr(Key, key_as_string, None)
    return key_object

secondary_capture_key_object = get_key_object(secondary_capture_key_as_string)
termination_key_object = get_key_object(termination_key_as_string)

def on_keyboard_press(key):
    global control_pressed
    if key == secondary_capture_key_object:  
        control_pressed = True
    elif key == termination_key_object:
        print_message("terminationMessage")
        terminate_event.set()
        return False 

def on_keyboard_release(key):
    global control_pressed
    if key == secondary_capture_key_object:  
        control_pressed = False

def on_mouse_click(mouse_x, mouse_y, button, pressed):
    global current_step
    if terminate_event.is_set():
        return False  
    
    if pressed and control_pressed: 
        active_window = pygetwindow.getActiveWindow()
        if active_window:
            window_box = active_window.left, active_window.top, active_window.right, active_window.bottom
        else:
            print_message("noActiveWindowFound")
            return

        screenshot = ImageGrab.grab(bbox=window_box)

        if screenshot is None:
            print_message("screenshot.failedToSave")
            return
        
        screenshot = draw_text_box(screenshot)
        draw = ImageDraw.Draw(screenshot)
       
        screen_width, screen_height = pygetwindow.getWindowsWithTitle(active_window.title)[0].width, pygetwindow.getWindowsWithTitle(active_window.title)[0].height
        
        arrow_angle = get_arrow_direction((mouse_x, mouse_y), screen_width, screen_height)

        end_x = mouse_x + 40 * math.cos(arrow_angle)
        end_y = mouse_y + 40 * math.sin(arrow_angle)
        
        draw_arrow(draw, (mouse_x, mouse_y), (end_x, end_y))

        saving_path = f"{output_directory}/step-{current_step}.png"
        screenshot.save(saving_path)
        print_message("screenshot.saved", path=saving_path)
        current_step += 1

def start_listening_mouse():
    with MouseListener(on_click=on_mouse_click) as mouse_listener:
        mouse_listener.join()

def start_listening_keyboard():
    with KeyboardListener(on_press=on_keyboard_press, on_release=on_keyboard_release) as keyboard_listener:
        keyboard_listener.join()

def main():
    # Run listeners in separate threads
    mouse_thread = threading.Thread(target=start_listening_mouse)
    keyboard_thread = threading.Thread(target=start_listening_keyboard)

    mouse_thread.start()
    keyboard_thread.start()

    mouse_thread.join()
    keyboard_thread.join()

if __name__ == "__main__":
    main()
