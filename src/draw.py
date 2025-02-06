import math

import configparser

config_parser = configparser.ConfigParser()
config_parser.read('config.ini')

from PIL import ImageDraw, ImageGrab, Image

def calculate_arrowhead_positions(end: tuple, angle: float, arrow_length=15):
    end_x, end_y = end
    arrow_head_left = (end_x - arrow_length * math.cos(angle - math.pi / 4),
                       end_y - arrow_length * math.sin(angle - math.pi / 4))
    arrow_head_right = (end_x - arrow_length * math.cos(angle + math.pi / 4),
                        end_y - arrow_length * math.sin(angle + math.pi / 4))
    return arrow_head_left, arrow_head_right

from configuration import get_color_from_config_parser

def draw_arrow(draw, start: tuple, end: tuple, arrow_length=15, arrow_width=3):
    start_x, start_y = start
    end_x, end_y = end

    arrow_color = get_color_from_config_parser("arrow") 
    draw.line([start_x, start_y, end_x, end_y], fill=arrow_color, width=arrow_width)
    angle = math.atan2(end_y - start_y, end_x - start_x)

    arrow_head_left, arrow_head_right = calculate_arrowhead_positions(end, angle, arrow_length)
    draw.line([arrow_head_left, (end_x, end_y)], fill=arrow_color, width=arrow_width)
    draw.line([arrow_head_right, (end_x, end_y)], fill=arrow_color, width=arrow_width)

def draw_text_box(draw, width, height, new_height):
    text_box_color = get_color_from_config_parser("text_box")
    draw.rectangle([0, height, width, new_height], fill=text_box_color)

def draw_new_screenshot(window_box):
    screenshot = ImageGrab.grab(bbox=window_box)
    width, height = screenshot.size
    new_height = height + config_parser.getint("text_box", "height")
    new_screenshot = Image.new("RGB", (width, new_height), (255, 255, 255))  # Create new blank image
    new_screenshot.paste(screenshot, (0, 0))
    draw = ImageDraw.Draw(new_screenshot) 
    return draw    