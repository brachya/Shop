import socket
from threading import Lock, Thread
import sys

# import validate
from tree import Tree, Node


class ShopServer:
    clients: list[socket.socket] = []
    IP = "127.0.0.1"
    PORT = 34500
    MUTEX = Lock()

    def __init__(self, file_path: str) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen(5)
        print("server starting...")
        self.file_path = file_path
        self.tree = Tree()
        self.csv_import(
            self.tree, "name"
        )  # name, last name, identity, phone, date, dept

    def start_connection(self) -> None:
        try:
            cli_sock, cli_add = self.server_socket.accept()
        except ConnectionResetError:
            quit()
        else:
            print(f"Client {cli_add} connected")
            self.clients.append(cli_sock)
            Thread(target=self.connection_handle, args=(cli_sock, cli_add)).start()

    def csv_import(self, binary_tree: Tree, orderby: str) -> None:
        print("csv importing")
        customers = self.open_file()
        for customer in customers:
            binary_tree.add_node(
                Node(
                    customer["first name"],  # type: ignore
                    customer["last name"],  # type: ignore
                    customer["id"],  # type: ignore
                    customer["phone"],  # type: ignore
                    customer["date"],  # type: ignore
                    customer["dept"],  # type: ignore
                ),
                orderby,
            )

    def open_file(self) -> list[dict[str, str | int]]:
        with open(self.file_path, "r", encoding="UTF-8") as csv:  # encoding for hebrew
            non_ordered_data: list[str] = csv.read()[1:-1].split("\n")
            data: list[dict[str, str | int]] = [
                self.customer_str_to_dict(customer) for customer in non_ordered_data
            ]
            return data

    def customer_str_to_dict(self, customer: str) -> dict[str, str | int]:
        print(customer)
        customer_lst: list[str] = customer.split(",")
        print(customer_lst)
        fn: str = customer_lst[0]
        ln: str = customer_lst[1]
        identity: int = int(customer_lst[2])
        phn: int = int(customer_lst[3])
        dt: str = customer_lst[4]
        dp: int = int(customer_lst[5])
        return {
            "first name": fn,
            "last name": ln,
            "id": identity,
            "phone": phn,
            "date": dt,
            "dept": dp,
        }

    def connection_handle(
        self, client_socket: socket.socket, client_address: tuple[str, int]
    ) -> None:
        while True:
            message = client_socket.recv(1024).decode("UTF-8").split()
            if message[0] == "select":
                result = self.tree.find_node_recursive(message[1], "name")
                if not result:
                    client_socket.sendall("No Result".encode())
                else:
                    client_socket.sendall("result".encode())
                continue


if __name__ == "__main__":
    shop = ShopServer(sys.argv[1])
    while True:
        shop.start_connection()
