"""
Usage of the FindFiles function of the win32api with my WIN32_FIND_DATA class
Getting information with the FindFiles function, then processing them with WIN32_FIND_DATA class for clear output
Author: Kacy538 (ycaK)
"""

import win32api

from FindFiles import WIN32_FIND_DATA

x = win32api.FindFiles('test_file.txt')

dataProcessing = WIN32_FIND_DATA.Resolve(x)

dataProcessing.display_all()
