import pyautogui
import numpy as np
import cv2
import time
import pyautogui
from mss import mss
import glob
import threading
import queue

# Finds game's region2
dino = pyautogui.locateOnScreen('./assets/t1.png')
# If game region found
if dino is not None:
    boxX = dino.lef + 10
    boxY = dino.top + 10
    pyautogui.moveTo(boxX,boxY)
    pyautogui.click()
    time.sleep(2)
else:
    print('Initial game region is not found. '
          '\nError is either game is not open or on wrong menu.'
          '\nStart game on fresh start before running.')
