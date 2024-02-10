import socket

ip = "127.0.0.1"
p = 34500
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((ip, p))
while True:
    c.sendall(input("==> ").encode())
    print(c.recv(1024).decode())
c.close()
