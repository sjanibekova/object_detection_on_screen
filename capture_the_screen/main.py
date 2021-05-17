import cv2 as cv
import numpy as np
import os
from time import time
from windowCapture import WindowCapture
import pyautogui
from vision import Vision

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# initialize the WindowCapture class
wincap = WindowCapture('Calculator')
print(WindowCapture.list_window_names())
print(wincap.get_element_tree())
vision_limestone = Vision('seven.jpg')
print(vision_limestone)


loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    points = vision_limestone.find(np.array(screenshot), 0.8, 'rectangles')

    cv.imshow('Computer Vision', np.array(screenshot))

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')