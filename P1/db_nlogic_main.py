from db_main import *
import _thread
import time

class NLogic(object):
    DEBUG_MODE = False

    def __init__(self):
        self.IP = '127.0.0.1'
        self.PORT = 8292
        self.net_logic = socket.socket()

    def init_all(self):
        self.net_logic.bind((self.IP, self.PORT))
        self.net_logic.listen()

    def run(self):
        self.init_all()
        self.main_loop()

    def main_loop(self):
        while True:
            conn, addr = self.net_logic.accept()
            _thread.start_new_thread(self.handle, (conn,))
            if self.DEBUG_MODE == True:
                print('Got connection from > ' + addr[0] + ':' + str(addr[1]) + '\n')

    def handle(self, conn):
        while True:
            error_message = False
            try:
                data = conn.recv(1024)
                if self.DEBUG_MODE == True:
                    print(data, "<- = conn.recv(1024)")
            except:
                if self.DEBUG_MODE == True:
                    print("\nClient has disconnected hadly!\n")
                break
            if data == b'\r\n':
                if self.DEBUG_MODE == True:
                    print(data, "<- none of those")
                pass
            elif not data:
                break
            else:
                try:
                    data = data.decode()
                    data = data.split()
                    if self.DEBUG_MODE == True:
                        print(data, "<- decode and split")
                except:
                    if self.DEBUG_MODE == True:
                        print("\nClient has probably disconnected or problem with decodeing!\n")
                    break
                try:
                    if data[0] == 'help':
                        help()
                except:
                    if error_message == False:
                        if self.DEBUG_MODE == True:
                            help()
                        error_message = True
                try:
                    if data[0] == 'search' or data[0] == 'find': # search doesn't work
                        s_lookup = search_db(db_fixed_name, data[1])
                        s_lookup = str(s_lookup)
                        conn.send(s_lookup.encode())
                except:
                    if error_message == False:
                        if self.DEBUG_MODE == True:
                            print("[?] Try: search <username>\n[?] Or try: help")
                        error_message = True
                try:
                    if data[0] == 'acc_info':
                        lookup = read_acc_one(db_fixed_name, data[1])
                        if self.DEBUG_MODE == True:
                            print(lookup)
                        conn.send(lookup[0].encode())
                        conn.send(lookup[1].encode())
                        time.sleep(0.00000001) # Don't delete it
                        conn.send(lookup[2].encode())
                except:
                    if error_message == False:
                        if self.DEBUG_MODE == True:
                            print("[?] Try: acc_info <username>\n[?] Or try: help")
                        error_message = True
                try:
                    if data[0] == 'acc_info_all':
                        read_acc_all(db_fixed_name)
                except:
                    if error_message == False:
                        if self.DEBUG_MODE == True:
                            print("[?] Error...\n[?] Try: help")
                        error_message = True
                try:
                    if data[0] == 'add_acc':
                        write_acc_check(db_fixed_name, data[1], data[2])
                except:
                    if error_message == False:
                        if self.DEBUG_MODE == True:
                            print("[?] add_acc <username> <password>\n[?] Try: help")
                        error_message = True
                try:
                    if data[0] == 'del_acc':
                        del_acc(db_fixed_name, data[1])
                except:
                    if error_message == False:
                        if self.DEBUG_MODE == True:
                            print("[?] Try: del_acc <username>\n[?] Or try: help")
                        error_message = True
        if self.DEBUG_MODE == True:
            print("\nClient disconnected!\n")

try:
    print("Starting server...\n")
    network_logic = NLogic()
    network_logic.run()
except:
    print("Error starting server!")