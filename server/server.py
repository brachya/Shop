import socket
from threading import Lock, Thread
import sys
from validate import Validate
from tree import Tree, Node


class ShopServer:
    clients: list[socket.socket] = []
    IP = "127.0.0.1"
    PORT = 34500
    MUTEX = Lock()

    def __init__(self, file_path: str) -> None:
        # starting server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen(5)
        print("server starting...")
        self.file_path = file_path
        # creating trees
        self.tree_by_name = Tree()
        self.tree_by_last_name = Tree()
        self.tree_by_id = Tree()
        self.tree_by_phone = Tree()
        self.tree_by_date = Tree()
        self.tree_by_dept = Tree()
        # define trees
        self.csv_import(self.tree_by_name, "name")
        self.csv_import(self.tree_by_last_name, "last_name")
        self.csv_import(self.tree_by_id, "identity")
        self.csv_import(self.tree_by_phone, "phone")
        self.csv_import(self.tree_by_date, "date")
        self.csv_import(self.tree_by_dept, "dept")

    def validation(self, customer: str) -> list[str] | str:
        customer_details: list[list[str]] = [c.split("=") for c in customer.split(",")]
        details = [s[1] for s in customer_details]
        to_valid = Validate(details)
        valid = to_valid.checked()
        del to_valid
        if valid == "True":
            return details
        return valid  # in case of errors

    def id_exist(self, identity: int) -> bool:
        return (
            True if self.tree_by_id.find_node_recursive(identity, "identity") else False
        )

    def set_new_customer(self, customer_details: list[str]) -> None:
        customer = Node(
            customer_details[0],
            customer_details[1],
            int(customer_details[2]),
            int(customer_details[3]),
            customer_details[4],
            int(customer_details[5]),
        )
        self.tree_by_name.add_node(customer, "name")
        self.tree_by_last_name.add_node(customer, "last_name")
        self.tree_by_id.add_node(customer, "identity")
        self.tree_by_phone.add_node(customer, "phone")
        self.tree_by_date.add_node(customer, "date")
        self.tree_by_dept.add_node(customer, "dept")

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
        print(f"csv importing to {orderby}")
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
        customer_lst: list[str] = customer.split(",")
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
            message = client_socket.recv(1024).decode("UTF-8")
            if message.startswith("select"):
                message = message.split()
                result: Node | None = self.tree_by_name.find_node_recursive(
                    message[1], "name"
                )
                if not result:
                    client_socket.sendall("No Result".encode())
                else:
                    client_socket.sendall("result".encode())
                continue
            elif message.startswith("set"):
                message = message[4:]
                valid: list[str] | str = self.validation(message)
                if type(valid) == type(""):
                    client_socket.sendall(valid.encode())
                    continue
                print(valid)
                identity = int(valid[3])
                if self.id_exist(identity):
                    client_socket.sendall(f"id {identity} already exist.".encode())
                    continue
                self.set_new_customer(valid)
                client_socket.sendall("customer successfully added.".encode())
            elif message.startswith("print"):
                all_customers = self.tree_by_name.print_tree()
                if all_customers:
                    client_socket.sendall(all_customers.encode())


if __name__ == "__main__":
    # shop = ShopServer(sys.argv[1])
    shop = ShopServer("server/db.csv")
    while True:
        shop.start_connection()
