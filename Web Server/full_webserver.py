"""
Project: Web Server
Description: Custom web server written with pure python libraries + logging of ip connections with server
Version: 1.5.3
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
Update Info v 1.4.2: Added reload function, to reload main thread
Update Info v 1.4.3: Added b as option for reading file to function "find_source_file()" so loading files with content other than english is possible
Update Info v 1.5: Moved CLI to another file and made reloading acquire new version of server with reload command
Update Info v 1.5.1: Now updates regarding CLI will be in CLI file
Update Info v 1.5.2: Fixed encoding files so it is now universal with small error handling
Update Info v 1.5.3: Moved logging clients to log only if _DEBUG is true
TODO: Add scripting language for client <--> server interaction
TODO: Move update feed to another file
"""

import time # Heading, error displaying and ip logging
import socket # Network operations
import os # Path operations
import _thread # Client handling
import sys # Error logging

class webServer:
    def __init__(self):
        self.ip = '127.0.0.1' # IP of the server
        self.port = 8080 # Port of the server
        self.servSocket = socket.socket() # Creating socket ( One time usage )
        self._ALIVE = False # Sets _ALIVE var to False
        self._VERSION = '1.5.3' # Version of server
        self._DEBUG = False # Debug mode

    def error_logger(self, function_name, error, date): # Logs errors
        with open('error.log', 'a') as error_logger:
            error_logger.writelines("\n[ * ] Date: " + str(date) + " [ ! ] Got error in function: " + str(function_name) + " - More info: " + str(str(error).encode(sys.stdout.encoding, errors='replace'))) # Write the error

    def client_logger(self, addr, site): # It can slow down server a bit if there are too many clients
        with open('client.log', 'a') as client_logger:
            data = 'Time: ' + str(time.strftime("%a, %d, %b, %H:%M:%S", time.localtime())) + ' IP: ' + str(addr[0]) + ' Directory: ' + str(site.decode().split()[1]) + '\n'
            client_logger.writelines(data)

    def generate_server_header(self, code): # Generates the heading of server
        if code == 200:
            try:
                servHead = b'HTTP/1.1 200 OK\n'
                servHead += b'Date: ' + time.strftime("%a, %d, %b, %Y, %H:%M:%S", time.localtime()).encode() + b'\n'
                servHead += b'Server: CODENAME - KACY\n'
                servHead += b'Connection: close\n\n'
                return servHead
            except Exception as error:
                self.error_logger('generate_server_header()', error, time.strftime(" [ %a, %d, %b, %H:%M:%S ]", time.localtime())) # Logs the error to file

    def generate_four_zero_four(self, link_name): # Generates the 404 website based on the name of the link
        website = b'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>Website not found!</title>\n</head>\n<body>\n<div>\n<h1>404! ' + str(link_name).encode() + b' doesn\'t exist!</h1>\n</div>\n</body>\n</html>\n'
        return website # Returns the website

    def find_source_file(self, file_name): # Searches for file then returns the content of it
        try:
            if '404' not in file_name: # If 404 is not in the file name ( got it from the rule set function as 404 error )
                # full_file_path = os.getcwd() + file_name # Get current path and sums it together with the file_name path
                try:
                    with open(os.getcwd() + file_name, 'r') as http_read: # Opens the file from the full path gotten from full_file_path var
                        return http_read.read() # Returns the content of the file
                except:
                    with open(os.getcwd() + file_name,'rb') as http_read:  # If the first cannot open this will ( Error Handling )
                        return http_read.read()  # Returns the content of the file
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
            elif '.ico' in cltReq.decode().split()[1]: # ICO rule
                web_querry = cltReq.decode().split()[1]
            elif '/' == cltReq.decode().split()[1]: # / rule
                web_querry = cltReq.decode().split()[1] + 'index.html'
            else: # All other extensions
                web_querry = '404' # The 404 error code
                return (web_querry, cltReq.decode().split()[1]) # Returns path with 404 file
            return web_querry # Returns the path from rule-set
        except Exception as error:
            self.error_logger('client_req_parser()', error, time.strftime(" [ %a, %d, %b, %H:%M:%S ]", time.localtime())) # Logs the error to file

    def response_crafting(self, heading, web_file): # Sums heading and content together, then returns it so it may be used by another function
        try:
            try:
                full_response = heading + web_file # Sums heading and content together
            except:
                full_response = heading + web_file.encode() # If first doesn't work this will ( Error Handling )
            return full_response # Returns the ready request
        except Exception as error:
            self.error_logger('response_crafting()', error, time.strftime(" [ %a, %d, %b, %H:%M:%S ]", time.localtime()))

    def final_response_crafting(self, clntDt): # Takes client request then crafts and sends file to clients web browser
        try:
            main_website = self.find_source_file(self.client_req_parser(clntDt)) # Searches for file
            resp = self.response_crafting(self.generate_server_header(200), main_website) # Crafts response (heading + content)
            return resp # Returns the request to be sent
        except Exception as error:
            self.error_logger('final_response_crafting()', error, time.strftime(" [ %a, %d, %b, %H:%M:%S ]", time.localtime()))

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
                conn, addr = self.servSocket.accept() # Waits for new connection
                _thread.start_new_thread(self.run_server, (conn, addr)) # If there is new connection, then start new thread to handle it
            except Exception as error:
                self.error_logger('run()', error, time.strftime(" [ %a, %d, %b, %H:%M:%S ]", time.localtime()))
                continue

    def run_server(self, connSocket, addr): # Handles new clients
        try:
            clientData = connSocket.recv(1024) # Waiting for request from client
            connSocket.send(self.final_response_crafting(clientData)) # After parsing client's request, the data from it is used to get the website
            if self._DEBUG == True:
                self.client_logger(addr, clientData) # Logging client
            connSocket.close() # Closing connection
        except Exception as error:
            self.error_logger('run_server()', error, time.strftime(" [ %a, %d, %b, %H:%M:%S ]", time.localtime()))
            connSocket.close()