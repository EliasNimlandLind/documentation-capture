
import configparser

config_parser = configparser.ConfigParser()
config_parser.read('config.ini')

def get_color_from_config_parser(section):
    red, green, blue = bytes.fromhex(config_parser.get(section, "color"))
    color = (red, green, blue)
    return color