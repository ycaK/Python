"""
Program that scrolls your mouse over network (The Server)

Just run it | If client connects it will display in console: "Connected" |
If client disconnects it will display in console: "Disconnected"
Author: Kacy538 (ycaK)
"""
import win32api
import socket
import win32con
import time

x, y = 0, 0
IP, PORT = '127.0.0.1', 8522
SERVER = True

try:
    if SERVER:
        server = socket.socket()
        server.bind((IP, PORT))
        server.listen(1)
        conn, address = server.accept()
        print("Connected")
        while True:
            data = conn.recv(2)
            if not data:
                break
            if data.decode() == 'up':
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, 4, 0)
            if data.decode() == 'dn':
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, -4, 0)
except:
    print("Disconnected")
