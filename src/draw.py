import math
import configparser

from math_helper import get_arrowhead_positions

config_parser = configparser.ConfigParser()
config_parser.read('config.ini')

from PIL import ImageDraw, ImageGrab, Image

def get_color_from_config_parser(section):
    hex_color = config_parser.get(section, "color").strip("#")
    red, green, blue = bytes.fromhex(hex_color)
    return red, green, blue

def draw_arrow(draw, start: tuple, end: tuple, arrow_length=15, arrow_width=3):
    start_x, start_y = start
    end_x, end_y = end

    arrow_color = get_color_from_config_parser("arrow") 
    draw.line([start_x, start_y, end_x, end_y], fill=arrow_color, width=arrow_width)
    angle = math.atan2(end_y - start_y, end_x - start_x)

    arrow_head_left, arrow_head_right = get_arrowhead_positions(end, angle, arrow_length)
    draw.line([arrow_head_left, (end_x, end_y)], fill=arrow_color, width=arrow_width)
    draw.line([arrow_head_right, (end_x, end_y)], fill=arrow_color, width=arrow_width)

# * Redundant
def draw_text_box(screenshot):      
    if config_parser.getboolean("text_box", "is_enabled"):
        width, height = screenshot.size
        new_height = height + config_parser.getint("text_box", "height")
        new_screenshot = Image.new("RGB", (width, new_height), get_color_from_config_parser("text_box"))  # Create new blank image

        # Paste original screenshot into new screenshot
        new_screenshot.paste(screenshot, (0, 0))
        return new_screenshot  # Return the new screenshot with the pasted image
    else:
        return screenshot  # If not enabled, return the original screenshot



def draw_new_screenshot(window_box):
    screenshot = ImageGrab.grab(bbox=window_box)
    width, height = screenshot.size
    new_height = height + config_parser.getint("text_box", "height")
    new_screenshot = Image.new("RGB", (width, new_height), (255, 255, 255))  # Create new blank image
    new_screenshot.paste(screenshot, (0, 0))
    draw = ImageDraw.Draw(new_screenshot) 
    return draw    