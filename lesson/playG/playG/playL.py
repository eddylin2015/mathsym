import time

from pynput.keyboard import Key, Controller

sleep_per_step=2

keyboard = Controller()
keyboard.press(Key.alt)
keyboard.press(Key.tab)
time.sleep(sleep_per_step)
keyboard.release(Key.tab)
keyboard.release(Key.alt)

for i in range(207):
    
    keyboard.press(Key.alt)
    keyboard.press(Key.f12)
    time.sleep(1)
    keyboard.release(Key.f12)
    keyboard.release(Key.alt)

    time.sleep(sleep_per_step)
    keyboard.press(Key.left)
    time.sleep(1)
    keyboard.release(Key.left)

    

time.sleep(sleep_per_step)



"""
from pynput.mouse import Button, Controller
mouse = Controller()
print(f'The curr_pointer position is {mouse.position}')
mouse.position = (200, 200) # Set pointer position
mouse.press(Button.left)
print(f'Now we have moved it to {mouse.position}')
mouse.move(100, 100) # Move pointer relative to current position
mouse.release(Button.left)
mouse.position = (300, 200)
mouse.press(Button.left)
mouse.move(-100, 100)
mouse.release(Button.left)
# Press and release
"""