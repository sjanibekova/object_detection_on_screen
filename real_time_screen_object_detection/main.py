# main.py
import cv2 as cv
import numpy as np
from time import time
from windowCapture import WindowCapture
from vision import findClickPositions
import numpy

wincap = WindowCapture('Calculator')
loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()


    cv.imshow('Computer Vision', np.array(screenshot))
    screenshot = np.array(screenshot)
    points = findClickPositions(
        'seven.jpg',
        screenshot,0.60,
        'rectangles')

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
#     # print(screenshot)

#
#     # debug the loop rate
#     print('FPS {}'.format(1 / (time() - loop_time)))
#     loop_time = time()
#
#     # press 'q' with the output window focused to exit.
#     # waits 1 ms every loop to process key presses
#     if cv.waitKey(1) == ord('q'):
#         cv.destroyAllWindows()
#         break
#
# print('Done.')