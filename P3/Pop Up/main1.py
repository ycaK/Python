"""
Simple pop up program that takes input from user
By pressing: Yes, No or Cancel the program saves the input to _CLICKEVENT and the proceeds to if else statements
Author: Kacy538 (ycaK)
"""


import win32api
import win32con

_PyHANDLE = 0
_TITLE = 'Title'
_MESSAGE = 'Message'
_MODE = win32con.MB_YESNOCANCEL

_CLICKEVENT = win32api.MessageBox(_PyHANDLE, _MESSAGE, _TITLE, _MODE)

if _CLICKEVENT == 6:
    print("User pressed: Yes")
elif _CLICKEVENT == 7:
    print("User pressed: No")
elif _CLICKEVENT == 2:
    print("User pressed: Cancel")
