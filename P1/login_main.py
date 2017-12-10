import socket
import _thread # TODO: Use it!

class LoginServer(object):
    DB_IP, DB_PORT = '127.0.0.1', 8292
    LOGIN_IP, LOGIN_PORT = '127.0.0.1', 8393
    TEMP_USERNAME, TEMP_PASSWORD, TEMP_UID = '', '', ''

    def __init__(self):
        self.net_logon = socket.socket()
        self.net_logon.bind((self.LOGIN_IP, self.LOGIN_PORT))
        self.net_logon.listen()

    def decode(self): # Cus I'm lazy
        global TEMP_USERNAME, TEMP_PASSWORD, TEMP_UID
        TEMP_USERNAME, TEMP_PASSWORD, TEMP_UID = TEMP_USERNAME.decode(), TEMP_PASSWORD.decode(), TEMP_UID.decode()

    def username_check(self, username):
        with socket.socket() as usr_check:
            usr_check.connect((self.DB_IP, self.DB_PORT))
            data = "find" + ' ' + username
            data = data.encode()
            usr_check.send(data)
            data_x = usr_check.recv(1024)
            if data_x.decode() == 'False':
                #print("User not in database!") # Add debug mode to the print commands
                return False
            elif data_x.decode() == 'True':
                #print("User in database!")
                return True
            usr_check.close()

    def login(self, username, password): # For DB Use
        global TEMP_USERNAME, TEMP_PASSWORD, TEMP_UID
        with socket.socket() as login:
            check = self.username_check(username)
            if check == True:
                login.connect((self.DB_IP, self.DB_PORT))
                data = 'acc_info' + ' ' + username
                login.send(data.encode())
                TEMP_USERNAME = login.recv(1024)
                #print(TEMP_USERNAME)
                TEMP_PASSWORD = login.recv(1024)
                #print(TEMP_PASSWORD)
                TEMP_UID = login.recv(1024)
                #print(TEMP_UID)
                self.decode() # Decodes data from binary to str
                if TEMP_USERNAME == username and TEMP_PASSWORD == password:
                    print(TEMP_USERNAME + " logged in successfully!")
                    return TEMP_UID
                else:
                    #print("Your Username or Password isn't correct!")
                    return 6
            elif check == False:
                #print("Wrong username")
                return 6

    def register(self, username, password): # For DB Use
        check = self.username_check(username)
        if check == False:
            with socket.socket() as register:
                register.connect((self.DB_IP, self.DB_PORT))
                data = 'add_acc' + ' ' + username + ' ' + password
                register.send(data.encode())
                register.close()
                return 4
        elif check == True:
            return 5

    def run(self):
        self.login_server()

    def login_server_handle(self, conn):
        # Codes: 1 = login, 2 = register, 3 = error | Register Codes: 4 = Registered, 5 = Username taken | Login Codes: 6 = Incorrect Password or Username, 7 = Correct UID, 8 = Incorrect UID
        try:
            choice = conn.recv(1024)
            choice = choice.decode()
        except:
            choice = ''
        if choice == 'login':
            conn.send('1'.encode())
            TMP_CLNT_USERNAME = conn.recv(1024)

            #################################################### Putty
            if TMP_CLNT_USERNAME == b'\r\n':
                TMP_CLNT_USERNAME = conn.recv(1024)
                if TMP_CLNT_USERNAME == b'\r\n':
                    TMP_CLNT_USERNAME = conn.recv(1024)
            #################################################### \Putty

            TMP_CLNT_PASSWORD = conn.recv(1024)

            #################################################### Putty
            if TMP_CLNT_PASSWORD == b'\r\n':
                TMP_CLNT_PASSWORD = conn.recv(1024)
                if TMP_CLNT_PASSWORD == b'\r\n':
                    TMP_CLNT_PASSWORD = conn.recv(1024)
            ##################################################### \Putty

            TMP_CLNT_USERNAME, TMP_CLNT_PASSWORD = TMP_CLNT_USERNAME.decode(), TMP_CLNT_PASSWORD.decode()
            TMP_CLNT_UID = self.login(TMP_CLNT_USERNAME, TMP_CLNT_PASSWORD)

            if TMP_CLNT_UID == 6:
                print(str(self.addr[0]) + " entered wrong username or password!") # C8
                conn.send('8'.encode())
            else:
                conn.send('7'.encode())
                conn.send(TMP_CLNT_UID.encode()) # C7
        elif choice == 'register':
            conn.send('2'.encode())
            TMP_CLNT_USERNAME = conn.recv(1024) # <

            #################################################### Putty

            if TMP_CLNT_USERNAME == b'\r\n':
                TMP_CLNT_USERNAME = conn.recv(1024)
                if TMP_CLNT_USERNAME == b'\r\n':
                    TMP_CLNT_USERNAME = conn.recv(1024)
            #################################################### \Putty

            TMP_CLNT_PASSWORD = conn.recv(1024) # <
            #################################################### Putty

            if TMP_CLNT_PASSWORD == b'\r\n':
                TMP_CLNT_PASSWORD = conn.recv(1024)
                if TMP_CLNT_PASSWORD == b'\r\n':
                    TMP_CLNT_PASSWORD = conn.recv(1024)
            ##################################################### \Putty

            TMP_CLNT_USERNAME, TMP_CLNT_PASSWORD = TMP_CLNT_USERNAME.decode(), TMP_CLNT_PASSWORD.decode()
            code = self.register(TMP_CLNT_USERNAME, TMP_CLNT_PASSWORD)
            if code == 4:
                print(TMP_CLNT_USERNAME + " has been successfully registered!")
                conn.send('4'.encode())
            elif code == 5:
                #print("This username is un-available!")
                conn.send('5'.encode())
        else:
            try:
                conn.send('3'.encode())
            except:
                pass

    def login_server(self):
        while True:
            try:
                conn, addr = self.net_logon.accept()
                self.addr = addr
                _thread.start_new_thread(self.login_server_handle, (conn,))
            except:
                print("Error in: login_server()")

serv = LoginServer()

serv.run()