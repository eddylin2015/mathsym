import pyautogui
import numpy as np
import cv2
import time
import pyautogui
from mss import mss
import glob
import threading
import queue

assets_path="./assets/objects_v/"
proximity_line_init_value = 170 
duck_time_init_value = 0.25
dino_top_off_set=  65

object_detected = False
proximity = proximity_line_init_value
duck_time = duck_time_init_value
scale_percent = 100 
scale_src_rate= int(100/scale_percent)
threshold = 0.50

### 
def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

####down or jump
def action(thread_name, q):
    while True:
        do_actions = q.get()
        if do_actions is None:
            # kill switch
            break

        if object_detected is True:
            if do_actions[0] is True:
                pyautogui.keyDown('down')
                time.sleep(duck_time)
                pyautogui.keyUp('down')
                #pyautogui.press('space')
            elif do_actions[1] is True:
                pyautogui.press('space')
        while object_detected is True:
            pass

###
def game(thread_name, x, y, q):
    global duck_time
    global proximity  # default jump distance from collision objects
    global threshold  # template accuracy threshold 0.7
    start_time = time.time()

    # Reads in all collision object files
    files = glob.glob(f'{assets_path}*.png')
    templates = []
    for file in files:
        temp = cv2.imread(file, 0)
        temp = cv2.Canny(temp, 25, 50)
        templates.append(temp)

    # imshow region
    sct = mss()
    ##600x150
    monitor = {'top': y, 'left': x, 'width': 500, 'height': 150- dino_top_off_set}

    last_time = time.time()
    while True:
        # Calculates how far away object should be from dino before dino jumps
        #  Based off game time length
        if (int(time.time() - start_time) + 1) % 45 == 0 and int(time.time() - start_time) < 300:
            proximity += 1.25
            duck_time += 0.001

        # Gets screen
        screen = np.asarray(sct.grab(monitor))
        ###
        if scale_percent < 100 :
            width = int(screen.shape[1] * scale_percent / 100)
            height = int(screen.shape[0] * scale_percent / 100)
            dim = (width, height)
            ## resize image
            screen = cv2.resize(screen, dim, interpolation=cv2.INTER_AREA)
        ###

        ### Prints time between frames
        #fps = str(int(1.0 / (time.time() - last_time)))
        #cv2.putText(screen, fps, (0, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        #last_time = time.time()

        ## Convert input screen to grey
        screen_grey = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        ## Convert to canny
        screen_canny = cv2.Canny(screen_grey, 25, 50)
        ## Convert to region of interest
        ##   Ignores dino, hi-score, and ground
        
        vertices = np.array([[65, 136], [65, 32], [600, 32], [600, 136]], np.int32)
        screen_roi = roi(screen_canny, [vertices])

        # Match finding for each template
        for template in templates:
            result = cv2.matchTemplate(screen_roi, template, cv2.TM_CCOEFF_NORMED)  # Match objects to screen
            width, height = template.shape[::-1]                                    # Get width/height of object
            locations = np.where(result >= threshold)                               # Get locations of object
            locations = list(zip(*locations[::-1]))                                 # Convert to x, y array

            # Groups overlapping rectangles
            #   Creates at least two rectangles to guarantee grouping
            rectangles = []
            for loc in locations:
                rect = [int(loc[0]), int(loc[1]), int(loc[0] + width), int(loc[1] + height)]
                rectangles.append(rect)
                rectangles.append(rect)
            rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

            # If objects exists on screen, draw & do actions
            global object_detected
            if len(rectangles):
                object_detected = True
                for (x, y, w, h) in rectangles:
                    cv2.rectangle(screen, (x, y), (w, h), (0, 0, 255), 1)       # Draws rectangles
                    # Checks if object is closing in on Dino on X axis
                    object_center = x + (width / 2)
                    if object_center < proximity:
                        # Checks whether if object near dino should be jumped over or ducked under
                        if (73-dino_top_off_set) < y < (83-dino_top_off_set):
                            # Duck, but not Jump
                            do_actions = [True, False]
                            q.put(do_actions)
                        elif y > (70-dino_top_off_set):
                            # Jump, but not Duck
                            do_actions = [False, True]
                            q.put(do_actions)
            else:
                object_detected = False

        # Draws detection line (Where objects are close enough to Dino for Dino q to jump)
        cv2.line(screen, (int(proximity), 0), (int(proximity), 150), (0, 255, 0), thickness=1)
        # Shows screen
        cv2.imshow('Chrome Dino', screen)
        # cv2.imshow('Canny + Roi', screen_roi)
        # Halts on button press q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            q.put(None)
            break
        if cv2.waitKey(1) & 0xFF == ord('r'):
            proximity = proximity_line_init_value
            duck_time = duck_time_init_value
            print("init.")

# Finds game's region2
dino = pyautogui.locateOnScreen('./assets/dino_start.png')
# If game region found
if dino is not None:
    boxX = dino.left
    boxY = dino.top - 150 * scale_src_rate + dino.height+20 *scale_src_rate + dino_top_off_set
    time.sleep(2)
    pyautogui.press('space')

    queue = queue.Queue()

    game_thread = threading.Thread(target=game, args=('game_thread', boxX, boxY, queue))
    actions_thread = threading.Thread(target=action, args=('actions_thread', queue))

    game_thread.start()
    actions_thread.start()
else:
    print('Initial game region is not found. '
          '\nError is either game is not open or on wrong menu.'
          '\nStart game on fresh start before running.')
