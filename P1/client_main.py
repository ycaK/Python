import socket

LOGIN_IP, LOGIN_PORT = '127.0.0.1', 8393
r_code = ''

while r_code != b'7':
    with socket.socket() as client:
        client.connect((LOGIN_IP, LOGIN_PORT))
        choice = input("login / register: ")
        choice = choice.encode()
        client.send(choice)
        code = client.recv(1024)
        if code == b'1':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            username, password = username.encode(), password.encode()
            client.send(username)
            client.send(password)
            r_code = client.recv(1024)
            if r_code == b'7':
                UID = client.recv(1024)
                print("You have logged in successfully!")
            elif r_code == b'8':
                print("Wrong username or password!")
            # Rest of the code! # The main app client side code!
        elif code == b'2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            username, password = username.encode(), password.encode()
            client.send(username)
            client.send(password)
            r_code = client.recv(1024)
            if r_code == b'4':
                print("You have been successfully registered!")
            elif r_code == b'5':
                print("This username is un-available!")
        elif code == b'3':
            print("Wrong command")