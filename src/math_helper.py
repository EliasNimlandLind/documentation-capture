import math

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

    arrow_direction = math.atan2(corner_y - mouse_y, corner_x - mouse_x)
    return arrow_direction