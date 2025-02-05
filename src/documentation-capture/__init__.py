import time
import os
import threading
import math
import configparser

import pygetwindow as pygetwindow
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key
from PIL import ImageGrab, ImageDraw, Image

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

def calculate_arrowhead_positions(end: tuple, angle: float, arrow_length=15):
    end_x, end_y = end
    arrow_head_left = (end_x - arrow_length * math.cos(angle - math.pi / 4),
                       end_y - arrow_length * math.sin(angle - math.pi / 4))
    arrow_head_right = (end_x - arrow_length * math.cos(angle + math.pi / 4),
                        end_y - arrow_length * math.sin(angle + math.pi / 4))
    return arrow_head_left, arrow_head_right

def draw_arrow(draw, start: tuple, end: tuple, arrow_length=15, arrow_width=3):
    start_x, start_y = start
    end_x, end_y = end
    draw.line([start_x, start_y, end_x, end_y], fill=(255, 0, 0), width=arrow_width)

    angle = math.atan2(end_y - start_y, end_x - start_x)
    
    arrow_head_left, arrow_head_right = calculate_arrowhead_positions(end, angle, arrow_length)

    draw.line([arrow_head_left, (end_x, end_y)], fill=(255, 0, 0), width=arrow_width)
    draw.line([arrow_head_right, (end_x, end_y)], fill=(255, 0, 0), width=arrow_width)

def distance(start_coordinates: tuple, end_coordinates: tuple):
    start_x, start_y = start_coordinates
    end_x, end_y = end_coordinates
    return math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)

def get_arrow_direction(point: tuple, screen_width, screen_height):
    mouse_x, mouse_y = point
    corners = [
        (0, 0),  # top-left corner
        (screen_width, 0),  # top-right corner
        (0, screen_height),  # bottom-left corner
        (screen_width, screen_height)  # bottom-right corner
    ]
    
    closest_corner = min(corners, key=lambda corner: distance(point, corner))
    
    corner_x, corner_y = closest_corner
    angle = math.atan2(corner_y - mouse_y, corner_x - mouse_x)
    
    return angle, closest_corner

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
        screenshot = ImageGrab.grab(bbox=window_box)
        width, height = screenshot.size

        new_height = height + config_parser.getint("text_box", "height")
        new_screenshot = Image.new("RGB", (width, new_height), (255, 255, 255))  # Create new blank image

        new_screenshot.paste(screenshot, (0, 0))

        rectangle_color = (255, 255, 255) 
        draw = ImageDraw.Draw(new_screenshot)
        draw.rectangle([0, height, width, new_height], fill=rectangle_color)

        screen_width, screen_height = pygetwindow.getWindowsWithTitle(active_window.title)[0].width, pygetwindow.getWindowsWithTitle(active_window.title)[0].height
        
        angle, closest_corner = get_arrow_direction((mouse_x, mouse_y), screen_width, screen_height)

        end_x = mouse_x + 40 * math.cos(angle)
        end_y = mouse_y + 40 * math.sin(angle)
        
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
    print("start")
    main()