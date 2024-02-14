# import socket


# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(("0.0.0.0", 12312))
# server_socket.listen(5)
# cli_sock, cli_add = server_socket.accept()
# print(type(cli_add[0]))
# print(type(cli_add[1]))


# print("s".isalnum())
# a = {"a": "ak", "b": "bk"}
# print(list(a.items()))


class A:
    def __init__(self, a: str) -> None:
        self._a = a

    def __str__(self) -> str:
        print(f"hello {self._a}")
        return ""


a = A("n")
print(a)
b = [a]
print(b)
# print(3 < 4)
# print("3b" > "3a")
