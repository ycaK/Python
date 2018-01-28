"""
Project: Web Server CLI
Description: Console Interface for Web Server
Version: 1.1
Python version: 3.6.4
Author: Kacy538 (ycaK)
Info: // X = Approved and working
Update Info v 1.1: Added dependencies for reload command and command help was added
"""

import full_webserver # Web Server
import os # os.system()
import time # time.sleep()
import socket # Shutting server down
import threading # Starting server
import importlib # Reloading server

_CLIVERSION = '1.1' # // X

def main(): # // X
    os.system("cls")  # Cleaning screen
    server = full_webserver.webServer()  # Making new object names server
    serverx = threading.Thread(None, server.run)  # Creating first thread
    while True:
        print("| Server Management Console |" + " Alive : " + str(serverx.is_alive()) + " | " + "Server version: " + server._VERSION + ' |')
        option = input("\n:> ") # Taking input from user
        if option == 'start' and serverx.is_alive() == False: # Starts the server if server is offline // X
            os.system("cls")
            server._ALIVE = True # Setting _ALIVE var to True
            serverx = threading.Thread(None, server.run) # Creating new thread
            serverx.start() # Starting new thread
            time.sleep(1.25)
            os.system("cls")
        elif option == 'stop' and serverx.is_alive() == True: # Stops the server  // X
            os.system("cls")
            print(" [ ! ] Stopping server !")
            time.sleep(0.5)
            os.system("cls")
            with socket.socket() as kill_serv: # Creating client to finish final request for the server
                server._ALIVE = False # Setting _ALIVE var to False
                kill_serv.connect((server.ip, server.port)) # Connecting to server
                kill_serv.close() # Disconnecting from server
                serverx.join() # Waiting for thread to join
        elif option == 'restart' and serverx.is_alive() == True: # Restarts the server if the server is online // X
            os.system("cls")
            print(" [ ! ] Restarting server !")
            with socket.socket() as kill_serv: # Creating client to finish final request for the server
                server._ALIVE = False # Setting _ALIVE var to False
                kill_serv.connect((server.ip, server.port)) # Connecting to server
                kill_serv.close() # Disconnecting from server
                serverx.join() # Waiting for thread to join
                server._ALIVE = True # Setting _ALIVE var to True
                serverx = threading.Thread(None, server.run) # Creating new thread
                serverx.start() # Starting new thread
                time.sleep(0.5)
                os.system("cls")
        elif option == 'status': # Displays current status of the server // X
            os.system("cls")
            print("|           STATUS           |")
            print("| [ * ] Thread Status: " + str(serverx.is_alive()) + '  |')
            print("| [ * ] Server Status: " + str(server._ALIVE) + '  |')
            input("\n[ Press enter to continue ... ]")
            os.system("cls")
        elif option == 'quit': # Quits CLI ( and server if not stopped earlier ) // X
            os.system("cls")
            print(" [ ! ] Exiting !")
            time.sleep(0.5)
            os.system("cls")
            os._exit(0)
        elif option == 'reload' and serverx.is_alive() == True: # Reloads the server file, if the server is online // X
            os.system("cls")
            print(" [ ! ] Reloading server ...")
            time.sleep(0.5)
            os.system("cls")
            with socket.socket() as kill_serv: # Creating client to finish final request for the server
                server._ALIVE = False # Setting _ALIVE var to False
                kill_serv.connect((server.ip, server.port)) # Connecting to server
                kill_serv.close() # Disconnecting from server
                serverx.join() # Waiting for thread to join
                importlib.reload(full_webserver) # Reloads full_webserver lib
                server = full_webserver.webServer()  # Making new object names server
        elif option == 'reload' and serverx.is_alive() == False: # Reloads the server, if the server is offline // X
            os.system("cls")
            print(" [ ! ] Reloading server ...")
            time.sleep(0.5)
            os.system("cls")
            importlib.reload(full_webserver)  # Reloads full_webserver lib
            server = full_webserver.webServer()  # Making new object names server
        elif option == 'help': # Prints out what each command do // X
            os.system("cls")
            print("| Available commands |")
            print("start: starts server")
            print("stop: stops server")
            print("restart: restarts server")
            print("reload: reloads server files")
            print("status: shows the status of the server")
            print("quit: shuts down server and quits CLI")
            print("version: shows version of CLI and server")
            input("\n[ Press enter to continue ... ]")
            os.system("cls")
        elif option == 'version': # Prints version of CLI and Server // X
            os.system("cls")
            print("| Version |")
            print("CLI: " + _CLIVERSION)
            print("Server: " + server._VERSION)
            input("\n[ Press enter to continue ... ]")
            os.system("cls")
        else: # Prints out all commands // X
            os.system("cls")
            print(" [ ? ] Commands: start, stop, restart, reload, status, version, help, quit")
            time.sleep(1)
            os.system("cls")

while True: # CLI Loop // X
    main()