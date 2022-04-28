import time

from pynput.keyboard import Key, Controller

sleep_per_step=1

keyboard = Controller()
keyboard.press(Key.alt)
keyboard.press(Key.tab)
time.sleep(sleep_per_step)
keyboard.release(Key.tab)
keyboard.release(Key.alt)

for i in range(55000):
    
    #keyboard.press(Key.alt)
    #keyboard.press(Key.f12)
    #time.sleep(0.1)
    #keyboard.release(Key.f12)
    #keyboard.release(Key.alt)
    #time.sleep(sleep_per_step)
    time.sleep(0.01)
    keyboard.press(Key.right)
    time.sleep(0.01)
    keyboard.release(Key.right)
   

time.sleep(sleep_per_step)
