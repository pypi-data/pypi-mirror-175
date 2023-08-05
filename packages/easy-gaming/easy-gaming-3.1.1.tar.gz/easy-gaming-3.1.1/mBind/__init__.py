import mouse
from pynput.keyboard import Key, Controller
import keyboard
import time

out_keyboard = Controller()

def change(in_button: str, out_button: str = 'left', stop_button: str = 's'):
    while True:
        if keyboard.is_pressed(in_button) or mouse.is_pressed(in_button):
            if out_button == 'left' or out_button == 'right' or out_button == 'middle':
                time.sleep(0.06)
                mouse.click(out_button)
            else:
                time.sleep(0.06)
                out_keyboard.press(out_button)
                out_keyboard.release(out_button)
        if keyboard.is_pressed(stop_button):
            break