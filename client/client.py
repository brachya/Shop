import socket

ip = "127.0.0.1"
p = 12312
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((ip, p))
c.close()
