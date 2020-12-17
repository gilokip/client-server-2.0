import socket
import select
import errno
import sys


#setting up constants
HEADER_LENGTH = 10
host = "127.0.0.1"
port = 1234

client_username = input("Username: ")
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((host, port))
c.setblocking(False)

username = client_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
c.send(username_header + username)

#sending basic info e.g username

while True:
    message = input(f"{client_username} > ")

    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode('utf-8')
        c.send(message_header + message)

    try:

#receiving data
        while True:
            username_header = c.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Server closed connection")
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            username = c.recv(username_length).decode('utf-8')

            message_header = c.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = c.recv(message_length).decode('utf-8')

            print(f"{username} > {message}")


    except IOError as e:
        if e.errno != errno.EAGAIN or e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('Error', str(e))
        sys.exit()
    

