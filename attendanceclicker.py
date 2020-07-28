from pynput import keyboard
import pyautogui

import configparser

key_combinations = {}
pressed_vk = set()
config = None

"""
These magic numbers came from just running a program that printed out the 
virtual key (vk) of each character as I pressed them

from pynput import keyboard

def on_press(key):
    vk = key.vk if hasattr(key, 'vk') else key.value.vk
    print('vk =', vk)

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
"""
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

def process_special_key_enum():
    """
    This grabs each of the non-alphanumeric from pynput and associates them with a human readable version to make configuring 
    key combos much easier. 
    """
    key_enum = keyboard.Key
    # key enums as a string look like Key.alt, this removes the 'Key.' prefix
    keys_without_prefix = map(lambda k: str(k)[4:], key_enum)
    zipped_keys = zip(keys_without_prefix, key_enum)
    return dict(zipped_keys)


def read_config():
    """
    This reads the configuration file and returns the config object for further processing later
    """
    config = configparser.ConfigParser()
    config.read('keyconfig.ini')

    return config


def parse_combo(combo):
    """
    This is a utility function for process_combos, we take a string from the config file and process it
    as a list of actual key objects that pynput understands.
    """
    keys = set()

    for k in combo.split('+'):
        if k in special_key_map:
            keys.add(special_key_map[k])
        else:
            keys.add(keyboard.KeyCode(vk=key_to_vk_map[k]))
    
    return keys


def process_combos(config):
    """
    Here we parse the keyconfig.ini file for key combinations to watch or as well as number of clicks
    per each action.

    frozenset creates an immutable set, this way we can use a combination of keys as a key for a dictionary
    to associate each combo to a number of clicks.
    """
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
    """
    This checks the hotkeys in the keyconfig.ini against the currently pressed input to see if we have pressed
    a given combination of keys
    """
    return all([get_vk(key) in pressed_vk for key in combo])
        

def click_mouse(number_of_clicks):
    """
    This is use to cause automatick clicks of the mouse, the mouse will click number_of_clicks times.
    """
    pyautogui.click(clicks=int(number_of_clicks))


def on_press(key):
    """
    This is how we capture key presses and see if we have pressed a combo
    """
    pressed_vk.add(get_vk(key))

    for combo in key_combinations:
        if is_combo_pressed(combo):
            click_mouse(key_combinations[combo])
            break


def on_release(key):
    """
    Here if a key is released and it is the escape key, we exit the program, if not we remove the released key from
    pressed_vk so we dont process it as part of a potential key combo press.
    """
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

