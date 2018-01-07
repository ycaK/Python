"""
Small program that shows how ClipCursor works
Makes the cursor stuck in the set position
Author: Kacy538 (ycak)
"""


import win32api

_LEFT = 1
_TOP = 1
_RIGHT = 1
_BOTTOM = 1

win32api.ClipCursor((_LEFT, _TOP, _RIGHT, _BOTTOM))
