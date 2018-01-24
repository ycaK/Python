"""
Project: Web Server
Description: Custom web server written with pure python libraries + logging of ip connections with server
Version: 1.0
Author: Kacy538 (ycaK)
Extra: Remember about adding index.html to each dir, for now html code of FSS website was used in index.html
Remember: KeyboardException can make false errors/warnings
TODO: Add scripting language for client <--> server interaction
"""

import time
import socket
import os
import _thread

class webServer:
    def __init__(self):
        self.ip = '127.0.0.1'
        self.port = 8080
        self.file_not_found = False
        self.servSocket = socket.socket()

    def generate_server_header(self, code):
        if code == 200 and self.file_not_found == False:
            try:
                servHead = 'HTTP/1.1 200 OK\n'
                servHead += 'Date: ' + time.strftime("%a, %d, %b, %Y, %H:%M:%S", time.localtime()) + '\n'
                servHead += 'Server: CODENAME - KACY\n'
                servHead += 'Connection: close\n\n'
                return servHead
            except:
                print("Error in header generating!")
                return 1
        else:
            self.file_not_found = False
            return 'HTTP/1.1 404 Not Found\n'

    def find_source_file(self, file_name):
        try:
            full_file_path = os.getcwd() + file_name
            with open(full_file_path, 'r') as http_read:
                return http_read.read()
        except:
            self.file_not_found = True
            return 'None'

    def client_req_parser(self, cltReq):
        try:
            if '.html' not in cltReq.decode().split()[1]:
                web_querry = cltReq.decode().split()[1] + 'index.html'
            else:
                web_querry = cltReq.decode().split()[1]
            return web_querry
        except:
            print("Error parsing clients request!")
            return "404.html"

    def response_crafting(self, heading, web_file):
        try:
            full_response = heading.encode() + web_file.encode('utf-8')
            return full_response
        except:
            print("Error in response crafting")

    def final_response_crafting(self, clntDt):
        main_website = self.find_source_file(self.client_req_parser(clntDt))
        return self.response_crafting(self.generate_server_header(200), main_website)

    def run(self):
        try:
            self.servSocket.bind((self.ip, self.port))
            print("Server started!")
        except:
            print("Error - Couldn't bind IP!")
            quit(1)

        self.servSocket.listen(0)
        print("Listening for connection ...")
        while True:
            try:
                with open('ip.log', 'a') as log_ip:
                    conn, addr = self.servSocket.accept()
                    log_ip.write('Client -> IP: '+ str(addr[0]) + ' PORT: ' + str(addr[1]) + '\n')
                    _thread.start_new_thread(self.run_server, (conn,))
            except:
                print("Error in run function!")
                continue


    def run_server(self, connSocket):
        try:
            clientData = connSocket.recv(1024)
            connSocket.send(self.final_response_crafting(clientData))
            connSocket.close()
        except:
            print("Error in run server!")
            connSocket.close()

x = webServer()
x.run() # Running server ...