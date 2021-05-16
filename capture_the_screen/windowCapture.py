import win32gui
import win32ui
import win32con
from ctypes import windll
from PIL import Image
import time
import ctypes
import pyautogui
from pywinauto import Desktop


# used for test

class WindowCapture:

    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, window_name=None):
        self.window_name = window_name
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:

            # find the handle for the window we want to capture
            self.hwnd_target = win32gui.FindWindow(None, window_name)

            if self.hwnd_target == 0:
                raise Exception("Window not found {} ".format(window_name))

    def get_screenshot(self):


        left, top, right, bot = win32gui.GetWindowRect(self.hwnd_target)
        w = right - left
        h = bot - top

        win32gui.SetForegroundWindow(self.hwnd_target)
        time.sleep(1.0)

        hdesktop = win32gui.GetDesktopWindow()
        hwndDC = win32gui.GetWindowDC(hdesktop)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hdesktop, hwndDC)

        if result == None:
            # PrintWindow Succeeded
            im.save("test.png")
        return im



    def get_element_tree(self):
        d = Desktop(backend='uia')
        print(d[self.window_name].print_control_identifiers())

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)




    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)