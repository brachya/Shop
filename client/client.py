import socket
from threading import Thread

ip = "127.0.0.1"
p = 34500
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((ip, p))


def recieving(client_socket: socket.socket):
    while True:
        try:
            print(client_socket.recv(1024).decode())
        except:
            break


Thread(target=recieving, args=(c,)).start()
while True:
    mess = input("==> ")
    try:
        c.sendall(mess.encode())
    except ConnectionResetError:
        print("500 server shuted off")
        break
    if mess == "bye":
        break
c.close()
