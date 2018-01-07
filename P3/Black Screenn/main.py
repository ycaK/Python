"""
Simple Program that makes screen go black
The screen will be black for _TIME seconds (+-)
Author: Kacy538 (ycaK)
"""


import win32api
import win32con
import time

_TIME = 10
delta = time.clock()

while int(time.clock()) - int(delta) + 2 != _TIME:
    win32api.ChangeDisplaySettings(win32api.EnumDisplaySettings(), win32con.CDS_RESET)
    win32api.ChangeDisplaySettings(win32api.EnumDisplaySettings(), win32con.CDS_FULLSCREEN)
