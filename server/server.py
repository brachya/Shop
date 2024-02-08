import socket
from threading import Lock, Thread
import sys


class ShopServer:
    clients: list[socket.socket] = []
    IP = "127.0.0.1"
    PORT = 34500
    MUTEX = Lock()

    def __init__(self, file_path: str) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen(5)
        self.file_path = file_path

    def start_connection(self) -> None:
        try:
            cli_sock, cli_add = self.server_socket.accept()
        except ConnectionResetError:
            quit()
        else:
            print(f"Client {cli_add} connected")
            self.clients.append(cli_sock)
            Thread(target=self.connection_handle, args=(cli_sock, cli_add))

    def open_file(self):
        with open(self.file_path, "r", encoding="UTF-8") as csv:  # encoding for hebrew
            non_ordered_data: list[str] = csv.read()[2:].split("\n")
            data: list[dict[str, str | int]] = [
                self.customer_str_to_dict(customer) for customer in non_ordered_data
            ]
            return data

    def customer_str_to_dict(self, customer: str):
        customer_lst: list[str] = customer.split(",")
        fn: str = customer_lst[0]
        ln: str = customer_lst[1]
        id: int = int(customer_lst[2])
        phn: int = int(customer_lst[3])
        dt: str = customer_lst[4]
        dp: int = int(customer_lst[5])
        return {
            "first name": fn,
            "last name": ln,
            "id": id,
            "phone": phn,
            "date": dt,
            "dept": dp,
        }

    @staticmethod
    def connection_handle(
        client_socket: socket.socket, client_address: tuple[str, int]
    ) -> None:
        while True:
            message = client_socket.recv(1024).decode("UTF-8")
            print(message)


if __name__ == "__main__":
    shop = ShopServer(sys.argv[1])
    while True:
        shop.start_connection()
