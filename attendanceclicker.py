from pynput import keyboard
import pyautogui

import configparser

key_combinations = {}
pressed_vk = set()
config = None

key_to_vk_map = {
    'a': 0,
    'b': 11,
    'c': 8,
    'd': 2,
    'e': 14,
    'f': 3,
    'g': 5,
    'h': 4,
    'i': 34,
    'j': 38,
    'k': 40,
    'l': 37,
    'm': 46,
    'n': 45,
    'o': 31,
    'p': 35,
    'q': 12,
    'r': 15,
    's': 1,
    't': 17,
    'u': 32,
    'v': 9,
    'w': 13,
    'x': 7,
    'y': 16,
    'z': 6,
    '0': 29,
    '1': 18,
    '2': 19,
    '3': 20,
    '4': 21,
    '5': 23,
    '6': 22,
    '7': 26,
    '8': 28,
    '9': 25,
}

special_key_map = {}

# This allows us to grab all the special keys (non-alphanumeric) and associate a human readable version of them with the enums
# this will allow us to allow the user to configure custom hotkeys
def process_special_key_enum():
    key_enum = keyboard.Key
    # key enums as a string look like Key.alt, this removes the 'Key.' prefix
    keys_without_prefix = map(lambda k: str(k)[4:], key_enum)
    zipped_keys = zip(keys_without_prefix, key_enum)
    
    return dict(zipped_keys)


def read_config():
    config = configparser.ConfigParser()
    config.read('keyconfig.ini')

    return config


def parse_combo(combo):
    keys = set()

    for k in combo.split('+'):
        if k in special_key_map:
            keys.add(special_key_map[k])
        else:
            keys.add(keyboard.KeyCode(vk=key_to_vk_map[k]))
    
    return keys


def process_combos(config):
    combos = config['KEY COMBOS']
    status_clicks = config['STATUS CLICKS']

    for combo in combos:
        parsed_combo = frozenset(parse_combo(combo))
        number_of_clicks = status_clicks[combos[combo]]
        key_combinations[parsed_combo] = number_of_clicks


def get_vk(key):
    """
    grabs the virtual key from the code from a key
    This allows us to ignore the case of the key passed (so we dont have to hit a then shift for shit + a hotkey)
    if we dont grab the vk and we hit shift + a it will pass shift + A and will ignore the combo if we are looking
    for a lower case a
    """
    return key.vk if hasattr(key, 'vk') else key.value.vk


def is_combo_pressed(combo):
    return all([get_vk(key) in pressed_vk for key in combo])
        

def click_mouse(number_of_clicks):
    pyautogui.click(clicks=int(number_of_clicks))


# this will choose the first combo that matches, so if you have one for shit + a and shift + alt + a then shift + a is the one triggered (maybe depening on the .ini file)
def on_press(key):
    pressed_vk.add(get_vk(key))

    for combo in key_combinations:
        if is_combo_pressed(combo):
            click_mouse(key_combinations[combo])
            break


def on_release(key):
    vk = get_vk(key)
    if vk in pressed_vk:
        pressed_vk.remove(vk)
    
    if key == keyboard.Key.esc:
        return False


if __name__ == '__main__':
    special_key_map = process_special_key_enum()
    config = read_config()

    process_combos(config)

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

