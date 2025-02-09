import json

with open("src/localization.json", "r", encoding="utf-8") as file:
    messages = json.load(file)

def get_nested_message(keys, message_dictionary):
    if not keys:
        return None 
    key = keys.pop(0)
    if key in message_dictionary:
        if isinstance(message_dictionary[key], dict):
            return get_nested_message(keys, message_dictionary[key])
        return message_dictionary[key]  
    return None

def print_message(key, **kwargs):
    keys = key.split(".")  # Support dot-separated keys for nested messages
    message_template = get_nested_message(keys, messages)
    
    if message_template is None:
        print(f"Unknown message key: {key}")
    else:
        print(message_template.format(**kwargs))