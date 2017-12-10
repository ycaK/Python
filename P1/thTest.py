import _thread
import socket

class Server(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sck = socket.socket()

    def run(self):
        self.binder()
        self.mloop()

    def binder(self):
        self.sck.bind((self.host, self.port))
        self.sck.listen(5)

    def mloop(self):
        while True:
            conn, addr = self.sck.accept()
            _thread.start_new_thread(self.handle, (conn,))
            print('Connected with ' + addr[0] + ':' + str(addr[1]))

    def handle(self, conn):
        conn.send("Hello!\r\n".encode())
        while True:
            data = conn.recv(4096)
            if data == b'\r\n':
                pass
            else:
                if not data:
                    print("Client has disconnected")
                    break
                else:
                    print("DATA: " + data.decode())
        conn.close()

t = Server('127.0.0.1', 2001)
t.run()