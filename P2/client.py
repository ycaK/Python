"""
Program that scrolls your mouse over network (The Client)

F7 (0x76) to scroll up | F8 (0x77) to scroll down | ESC (0x1B) to quit
Author: Kacy538 (ycaK)
"""

import win32api
import socket
import time

x, y = 0, 0
IP, PORT = '127.0.0.1', 8522
SERVER = False

if not SERVER:
    client = socket.socket()
    client.connect((IP, PORT))
    while True:
        if win32api.GetAsyncKeyState(0x76):
            client.send('up'.encode())
            client.send('stop'.encode())
            time.sleep(0.002)
        if win32api.GetAsyncKeyState(0x77):
            client.send('dn'.encode())
            client.send('stop'.encode())
            time.sleep(0.002)
        if win32api.GetAsyncKeyState(0x1B):
            quit(0)

