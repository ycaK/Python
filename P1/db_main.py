# Remember about: use always auto_csv()
# DONE: Create database engine
# TODO: Create server for database(DONE), Use some kind of multiprocessing in server(WON'T USE), Make server send a response
# UPDATE: Not using "multiprocessing", I've found out about handle method in threading library!
# INFO: Compatible with Putty for debugging

import csv # DB
import socket # For server stuff
import secrets # User-ID
import os # Deleting files

db_fixed_name = ''
user_token = ''
quit = False
IP, PORT = '127.0.0.1', 8292
DEBUG_MODE = False

def auto_csv(db_name):
    global db_fixed_name
    db_fixed_name = db_name
    if db_fixed_name == '':
        print("Can't be empty!")
    else:
        db_fixed_name = db_name + '.csv'

def token_gen():
    global user_token
    user_token = secrets.token_hex(8)

def clean_db(db_name):
    with open(db_name, 'w') as db_clean:
        if DEBUG_MODE == True:
            print("\n[!] DB Erased!\n")
        db_clean.close()

def read_acc_all(db_name):
    with open(db_name, newline='') as db_read_all:
        csv_read = csv.reader(db_read_all)
        print("\n" + "[ y ] --------------- [ y ]" + "\n")
        for acc in csv_read:
            if acc[0]:
                print("Username: " + acc[0])
            if acc[1]:
                print("Password: " + acc[1])
            if acc[2]:
                print("Permission level: " + acc[2])
                print("\n" + "[ x ] --------------- [ x ]" + "\n")

        #print("\n" + "[ x ] --------------- [ x ]" + "\n")
        db_read_all.seek(0)

def read_acc_one(db_name, name):
    with open(db_name) as db_read_once:
        not_found = True
        csv_read = csv.reader(db_read_once)
        for acc in csv_read:
            if acc[0] == name:
                if DEBUG_MODE == True:
                    print("\n" + "[ y ] --------------- [ y ]" + "\n")
                    print("Username: " + acc[0])
                    print("Password: " + acc[1])
                    print("Permission level: " + acc[2])
                    print("\n" + "[ x ] --------------- [ x ]" + "\n")
                not_found = False
                return acc[0], acc[1], acc[3]
        if not_found == True:
            print(name + " not found in db!")

def write_acc(db_name, name, password):
    with open(db_name, 'a', newline='') as db_write:
        csv_write = csv.writer(db_write)
        global user_token
        token_gen()
        csv_write.writerow([name, password, 'user', user_token])
        print(name + " created!")
        user_token = ''

def write_acc_check(db_name, name, password):
    with open(db_name) as db_read:
        create_acc = True
        csv_read = csv.reader(db_read)
        for acc in csv_read:
            if acc[0] == name:
                if DEBUG_MODE == True:
                    print(name + " is already in database!")
                create_acc = False
                return False
        if create_acc == True:
            write_acc(db_name, name, password)


def search_db(db_name, name):
    with open(db_name) as db_search:
        is_not = True
        csv_read = csv.reader(db_search)
        for acc in csv_read:
            if acc[0] == name:
                if DEBUG_MODE == True:
                    print(name + " is in db!")
                is_not = False
                return True
        if is_not == True:
            if DEBUG_MODE == True:
                print(name + " is not in db!")
            return False
        db_search.seek(0)

def del_acc(db_name, name):
    with open(db_name, 'r', newline='') as acc_read, open('new.csv', 'a', newline='') as acc_del:
        csv_read = csv.reader(acc_read)
        for row in csv_read:
            if name in row:
                pass
            else:
                csv_write = csv.writer(acc_del)
                csv_write.writerow(row)
                if DEBUG_MODE == True:
                    print(row)
        acc_read.seek(0)
        acc_del.seek(0)
        clean_db(db_name)
        acc_del.close()
        with open('new.csv', 'r', newline='') as acc_read2, open('acc.csv', 'a', newline='') as acc_write:
            csv_read2 = csv.reader(acc_read2)
            for row in csv_read2:
                csv_write2 = csv.writer(acc_write)
                csv_write2.writerow(row)
                if DEBUG_MODE == True:
                    print(row)
        acc_read2.close()
        if DEBUG_MODE == True:
            print('\n' + name + ' has been deleted from db!\n')
        os.remove('new.csv')
        if DEBUG_MODE == True:
            print("\nTemp file removed!\n")

def help():
    if DEBUG_MODE == True:
        print("\n[ H ] --------------- [ H ]\n")
        print("[ H ] search <username>")
        print("[ H ] acc_info <username>")
        print("[ H ] acc_info_all")
        print("[ H ] add_acc <username> <password>")
        print("[ H ] del_acc <username>")
        print("\n[ H ] --------------- [ H ]\n")

####    Only for local use (It only accepts one connection!     ####

def main(): # Server logic # Only for local use or debugging not for login server
    error_message = False
    auto_csv('acc')
    while quit == False:
        with socket.socket() as db:
            db.bind((IP, PORT))
            db.listen()
            conn, addr = db.accept()
            while True:
                error_message = False
                #data = input(":>")
                #data = data.encode()
                data = conn.recv(1024)
                print(data)
                if data == b'\r\n':
                    pass
                elif not data:
                    db.close()
                    break
                else:
                    data = data.decode()
                    data = data.split()
                    try:
                        if data[0] == 'help':
                            help()
                    except:
                        if error_message == False:
                            help()
                            error_message = True
                    try:
                        if data[0] == 'search':
                            search_db(db_fixed_name, data[1])
                    except:
                        if error_message == False:
                            print("[?] Try: search <username>\n[?] Or try: help")
                            error_message = True
                    try:
                        if data[0] == 'acc_info':
                            read_acc_one(db_fixed_name, data[1])
                    except:
                        if error_message == False:
                            print("[?] Try: acc_info <username>\n[?] Or try: help")
                            error_message = True
                    try:
                        if data[0] == 'acc_info_all':
                            read_acc_all(db_fixed_name)
                    except:
                        if error_message == False:
                            print("[?] Error...\n[?] Try: help")
                            error_message = True
                    try:
                        if data[0] == 'add_acc':
                            write_acc_check(db_fixed_name, data[1], data[2])
                    except:
                        if error_message == False:
                            print("[?] add_acc <username> <password>\n[?] Try: help")
                            error_message = True
                    try:
                        if data[0] == 'del_acc':
                            del_acc(db_fixed_name, data[1])
                    except:
                        if error_message == False:
                            print("[?] Try: del_acc <username>\n[?] Or try: help")
                            error_message = True

auto_csv('acc') # The one and only...

