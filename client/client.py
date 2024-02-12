import socket
from threading import Thread

IP = "127.0.0.1"
PORT = 34500
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))


def receiving(client_socket: socket.socket):
    while True:
        try:
            print(client_socket.recv(1024).decode())
        except:
            break


Thread(target=receiving, args=(client_socket,)).start()
while True:
    mess = input("==> ")
    if mess.startswith("set"):
        if not mess.count(",") == 5 or not mess.count("=") == 6:
            print("missing ',' or '='.")
            continue
    try:
        client_socket.sendall(mess.encode())
    except ConnectionResetError:
        print("500 server shuted off")
        break
    if mess == "bye":
        break
client_socket.close()
