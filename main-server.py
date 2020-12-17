import socket
import select

#setting up constants
HEADER_LENGTH = 10
host = "127.0.0.1"
port = 1234

#creating sockets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((host, port))
s.listen()

#creating client list
sockets_list = [s]

clients = {}


def receive_message(c):
    try:
        message_header = c.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": c.recv(message_length)}


    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == s:
            c, c_addr = s.accept()

            user = receive_message(c)
            if user is False:
                continue

            sockets_list.append(c)

            clients[c] = user

            print(f"New connection from {c_addr[0]}:{c_addr[1]} username:{user['data'].decode('utf-8')}")

        else:
            message = receive_message(notified_socket)

            if message is False:
                print(f"Connection closed from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            
            user = clients[notified_socket]
            print(f"New message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")


            for c in clients:
               if c != notified_socket:
                   c.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]