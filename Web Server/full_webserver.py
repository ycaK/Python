#  -*- coding: utf-8 -*-

"""
Project: Web Server
Description: Custom web server written with pure python libraries + logging of ip connections with server
Version: 1.4.1
Python version: 3.6.4
Author: Kacy538 (ycaK)
Extra: Remember about adding index.html to each dir, for now html code of FSS website was used in index.html
Remember: KeyboardException can make false errors/warnings
Update Info v 1.1: Added 404 error generation and rule set for accessing web file (now other files can't be browsed)
Update Info v 1.2: Fixed most bugs, added better exceptions and added time to logging ip, overall better interface
Update Info v 1.3: Added CLI to control server you can now do: start, stop, restart, status and quit
Update Info v 1.3.1: Added comments so code can be understood more easily
Update Info v 1.3.2: Improved CLI and added some more exceptions
Update Info v 1.4: Added basic logging of errors to file
Update Info v 1.4.1: Fixed logger, now fully working
TODO: Add scripting language for client <--> server interaction
TODO: Add logging errors to file
"""

import time # Heading, error displaying and ip logging
import socket # Network operations
import os # Path operations
import _thread # Client handling
import threading # CLI
import sys # Error logging

class webServer:
    def __init__(self):
        self.ip = '127.0.0.1' # IP of the server
        self.port = 8080 # Port of the server
        self.servSocket = socket.socket() # Creating socket ( One time usage )
        self._ALIVE = False # Sets _ALIVE var to False

    def error_logger(self, function_name, error, date):
        with open('error.log', 'a') as error_logger:
            error_logger.writelines("\n[ * ] Date: " + str(date) + " [ ! ] Got error in function: " + str(function_name) + " - More info: " + str(str(error).encode(sys.stdout.encoding, errors='replace'))) # Write the error

    def generate_server_header(self, code): # Generates the heading of server
        if code == 200:
            try:
                servHead = 'HTTP/1.1 200 OK\n'
                servHead += 'Date: ' + time.strftime("%a, %d, %b, %Y, %H:%M:%S", time.localtime()) + '\n'
                servHead += 'Server: CODENAME - KACY\n'
                servHead += 'Connection: close\n\n'
                return servHead
            except Exception as error:
                self.error_logger('generate_server_header()', error, time.strftime(" [ %a, %d, %b, %H:%M:%S ]", time.localtime())) # Logs the error to file

    def generate_four_zero_four(self, link_name): # Generates the 404 website based on the name of the link
        website = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>Website not found!</title>\n</head>\n<body>\n<div>\n<h1>404! ' + str(link_name) + ' doesn\'t exist!</h1>\n</div>\n</body>\n</html>\n'
        return website # Returns the website

    def find_source_file(self, file_name): # Searches for file then returns the content of it
        try:
            if '404' not in file_name: # If 404 is not in the file name ( got it from the rule set function as 404 error)
                full_file_path = os.getcwd() + file_name # Get current path and sums it together with the file_name path
                with open(full_file_path, 'r') as http_read: # Opens the file from the full path gotten from full_file_path var
                    return http_read.read() # Returns the content of the file
            else:
                return self.generate_four_zero_four(file_name[1]) # Returns the 404 website with the name of the tried link
        except:
            return self.generate_four_zero_four(file_name) # Returns the 404 website with the name of tried link

    def client_req_parser(self, cltReq): # Rule set, so only html, js and css files may be accessed by client
        try:
            if cltReq.decode().split() == []: # Sometimes client may send empty brackets
                return '[]' # Just returns anything
            elif '.html' in cltReq.decode().split()[1]: # HTML rule
                web_querry = cltReq.decode().split()[1]
            elif '.js' in cltReq.decode().split()[1]: # JS rule
                web_querry = cltReq.decode().split()[1]
            elif '.css' in cltReq.decode().split()[1]: # CSS rule
                web_querry = cltReq.decode().split()[1]
            elif '/' == cltReq.decode().split()[1]: # / rule
                web_querry = cltReq.decode().split()[1] + 'index.html'
            else: # All other extensions
                web_querry = '404' # The 404 error code
                return (web_querry, cltReq.decode().split()[1]) # Returns path with 404 file
            return web_querry # Returns the path from rule-set
        except Exception as error:
            self.error_logger('client_req_parser()', error, time.strftime(" [ %a, %d, %b, %H:%M:%S ]", time.localtime())) # Logs the error to file

    def response_crafting(self, heading, web_file): # Encodes heading and content, then Sums them together, then returns it so it may be used by another function
        try:
            full_response = heading.encode() + web_file.encode('utf-8') # Encodes heading and content then sums it together
            return full_response # Returns the summed and encoded ready request
        except Exception as error:
            self.error_logger('response_crafting()', error, time.strftime(" [ %a, %d, %b, %H:%M:%S ]", time.localtime()))

    def final_response_crafting(self, clntDt): # Takes client request then crafts and sends file to clients web browser
        main_website = self.find_source_file(self.client_req_parser(clntDt)) # Searches for file
        resp = self.response_crafting(self.generate_server_header(200), main_website) # Crafts response (heading + content)
        return resp # Returns the request to be sent

    def run(self): # Main function
        try:
            self.servSocket = socket.socket() # Creates again socket as first was closed after stopping server
            self.servSocket.bind((self.ip, self.port)) # Binds to selected ip and port
            print(" [ * ] Server started!") # Indicating that server has started
        except Exception as error:
            self.error_logger('run()', error, time.strftime(" [ %a, %d, %b, %H:%M:%S ]", time.localtime())) # Logs error to file
            return 0
        self.servSocket.listen(0) # Listen for clients
        print(" [ * ] Listening for connection ...")

        while True:
            if self._ALIVE != True:
                self.servSocket.close() # So new thread can be launched
                return 0 # To stop function
            try:
                with open('ip.log', 'a') as log_ip: # Open ip log file to log ip of clients after connecting
                    conn, addr = self.servSocket.accept() # Waits for new connection
                    log_ip.write('[ Client -> IP: '+ str(addr[0]) + ' PORT: ' + str(addr[1]) + ' ] - [ ' + time.strftime("%a, %d, %b, %H:%M:%S", time.localtime()) + ' ]' '\n') # Save clients ip and time of conection to file
                    _thread.start_new_thread(self.run_server, (conn,)) # If there is new connection, then start new thread to handle it
            except Exception as error:
                self.error_logger('run()', error, time.strftime(" [ %a, %d, %b, %H:%M:%S ]", time.localtime()))
                continue


    def run_server(self, connSocket): # Handles new clients
        try:
            clientData = connSocket.recv(1024) # Waiting for request from client
            connSocket.send(self.final_response_crafting(clientData)) # After parsing client's request, the data from it is used to get the website
            connSocket.close() # Closing connection
        except Exception as error:
            self.error_logger('run_server()', error, time.strftime(" [ %a, %d, %b, %H:%M:%S ]", time.localtime()))
            connSocket.close()

def main():
    os.system("cls")  # Cleaning screen
    server = webServer()  # Making new object names server
    serverx = threading.Thread(None, server.run)  # Creating first thread
    while True:
        print("| Server Management Console |" + " Alive : " + str(serverx.is_alive()) + " |")
        option = input("\n:> ") # Taking input from user
        if option == 'start' and serverx.is_alive() == False: # Starts the server
            os.system("cls")
            server._ALIVE = True # Setting _ALIVE var to True
            serverx = threading.Thread(None, server.run) # Creating new thread
            serverx.start() # Starting new thread
            time.sleep(1.25)
            os.system("cls")
        elif option == 'stop' and serverx.is_alive() == True: # Stops the server
            os.system("cls")
            print(" [ ! ] Stopping server !")
            time.sleep(0.5)
            os.system("cls")
            with socket.socket() as kill_serv: # Creating client to finish final request for the server
                server._ALIVE = False # Setting _ALIVE var to False
                kill_serv.connect((server.ip, server.port)) # Connecting to server
                kill_serv.close() # Disconnecting from server
                serverx.join() # Waiting for thread to join
        elif option == 'restart' and serverx.is_alive():
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
        elif option == 'status': # Displays current status of the server
            os.system("cls")
            print("|          STATUS          |")
            print(" [ * ] Thread Status: " + str(serverx.is_alive()))
            print(" [ * ] Server Status: " + str(server._ALIVE))
            time.sleep(1)
            os.system("cls")
        elif option == 'quit': # Quits CLI ( and server if not stopped earlier )
            os.system("cls")
            print(" [ ! ] Exiting !")
            time.sleep(0.5)
            os.system("cls")
            os._exit(0)
        else: # Prints out all commands
            os.system("cls")
            print(" [ ? ] Commands: start, stop, restart, status, quit")
            time.sleep(1)
            os.system("cls")

while True:
    main_thread = threading.Thread(None, target=main)
    main_thread.start()
    main_thread.join()