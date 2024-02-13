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
        self.tree_by_name = Tree("name")
        self.tree_by_last_name = Tree("last_name")
        self.tree_by_id = Tree("identity")
        self.tree_by_phone = Tree("phone")
        self.tree_by_date = Tree("date")
        self.tree_by_dept = Tree("dept")
        self.trees: dict[str, Tree] = {
            "name": self.tree_by_name,
            "last_name": self.tree_by_last_name,
            "identity": self.tree_by_id,
            "phone": self.tree_by_phone,
            "date": self.tree_by_date,
            "dept": self.tree_by_dept,
        }
        # define trees
        self.tree_to_tree()

    def validation(self, customer: str) -> list[str]:
        customer_details: list[list[str]] = [c.split("=") for c in customer.split(",")]
        details = [s[1] for s in customer_details]
        to_valid = Validate(details)
        valid = to_valid.checked()
        del to_valid
        details = ["true"] + details
        if valid[0] == "true":
            return details
        return valid  # in case of errors

    def customer_exist_update(self, new_details: list[str], customer: Node) -> str:
        error = ""
        if new_details[0] != customer.name:
            error += f"did you mean {customer.name}"
        if new_details[1] != customer.last_name:
            error += (
                f" {customer.last_name}"
                if error
                else f"did you mean last name {customer.last_name}"
            )
        if not error:
            self.customer_update(new_details, customer)  # type: ignore
            self.add_line_to_file(new_details)
            return f"customer {customer.name} on {customer.dept}"
        return error

    def customer_update(
        self, new_details: list[str], customer: Node, start: bool = False
    ) -> None:
        customer.dept = str(int(customer.dept) + int(new_details[5]))
        customer.date = str(new_details[4])
        if not start:
            self.tree_by_dept.remove_node(customer, customer.dept)
            self.tree_by_date.remove_node(customer, customer.date)
            customer.left["dept"] = None
            customer.right["dept"] = None
            customer.left["date"] = None
            customer.right["date"] = None
            self.tree_by_dept.add_node(customer)
            self.tree_by_date.add_node(customer)

    def add_line_to_file(self, customer_details: list[str]) -> None:
        with open(self.file_path, "a", encoding="UTF-8") as fw:
            fw.write(
                f"{customer_details[0]},{customer_details[1]},{int(customer_details[2])},{int(customer_details[3])},{customer_details[4]},{int(customer_details[5])}\n"
            )

    def set_new_customer(self, customer_details: list[str]) -> None:
        customer = Node(
            customer_details[0],
            customer_details[1],
            customer_details[2],
            customer_details[3],
            customer_details[4],
            customer_details[5],
        )
        for t in self.trees.keys():
            self.trees[t].add_node(customer)
        self.add_line_to_file(customer_details)

    def start_connection(self) -> None:
        try:
            cli_sock, cli_add = self.server_socket.accept()
        except ConnectionResetError:
            quit()
        else:
            print(f"Client {cli_add} connected")
            self.clients.append(cli_sock)
            Thread(target=self.connection_handle, args=(cli_sock, cli_add)).start()

    def csv_import(self, binary_tree: Tree, orderby: str) -> bool:
        print(f"csv importing to {orderby}")
        customers = self.open_file()
        if customers == [["empty"]]:
            return False  # in case that there is no values
        for customer in customers:
            exist = self.tree_by_id.find_node_recursive(customer[2])
            if exist:
                self.customer_update(customer, exist, True)
                continue
            binary_tree.add_node(
                Node(
                    customer[0],  # type: ignore
                    customer[1],  # type: ignore
                    customer[2],  # type: ignore
                    customer[3],  # type: ignore
                    customer[4],  # type: ignore
                    customer[5],  # type: ignore
                )
            )
        return True

    def tree_to_tree(self) -> None:
        if not self.csv_import(self.tree_by_id, "identity"):
            print("No customers")
            return
        all_nodes: list[Node] = self.tree_by_id.nodes()
        for tree in self.trees.keys():
            if tree == "identity":
                continue
            print(f"importing from identity tree to {tree} tree")
            for node in all_nodes:
                self.trees[tree].add_node(node)

    def fix_file(self, all: list[list[str | int] | str]) -> None:
        empty = 0
        for a in all:
            if a == "":
                empty += 1
        for _ in range(empty):
            all.remove("")
        with open(self.file_path, "w", encoding="UTF-8") as csv:  # encoding for hebrew
            for a in all:
                csv.write(a + "\n")  # type: ignore

    def open_file(self) -> list[list[str]]:
        with open(self.file_path, "r", encoding="UTF-8") as csv:  # encoding for hebrew
            non_ordered_data: list[str] = csv.read().split("\n")
            if "" in non_ordered_data:
                self.fix_file(non_ordered_data)  # type: ignore
                if "" in non_ordered_data:
                    return [["empty"]]
            data: list[list[str]] = [
                self.customer_str_to_list(customer) for customer in non_ordered_data
            ]
            return data

    def customer_str_to_list(self, customer: str) -> list[str]:
        customer_lst: list[str] = customer.split(",")
        fn: str = customer_lst[0]
        ln: str = customer_lst[1]
        identity: str = customer_lst[2]
        phn: str = customer_lst[3]
        dt: str = customer_lst[4]
        dp: str = customer_lst[5]
        return [fn, ln, identity, phn, dt, dp]

    def connection_handle(
        self, client_socket: socket.socket, client_address: tuple[str, int]
    ) -> None:
        while True:
            try:
                message = client_socket.recv(1024).decode("UTF-8")
            except ConnectionResetError:
                print(f"{client_address} shuted off")
                break
            if message.startswith("select"):
                message = message.split()
                result: Node | None = self.tree_by_name.find_node_recursive(message[1])
                if not result:
                    client_socket.sendall("No Result".encode())
                else:
                    client_socket.sendall("result".encode())
                continue
            elif message.startswith("set"):
                message = message[4:]
                valid: list[str] = self.validation(message)
                if valid[0] != "true":
                    client_socket.sendall(valid[0].encode())
                    continue
                valid = valid[1:]  # cut the 'true'
                customer_exist = self.tree_by_id.find_node_recursive(valid[2])
                if customer_exist:
                    resp = self.customer_exist_update(valid, customer_exist)
                    client_socket.sendall(resp.encode())
                    continue
                self.set_new_customer(valid)
                client_socket.sendall("customer successfully added.".encode())
            elif message.startswith("print"):
                message = message.split()
                if len(message) == 2:
                    all_customers = self.trees[message[1]].print_tree()
                else:
                    all_customers = self.tree_by_name.print_tree()
                if all_customers:
                    client_socket.sendall(all_customers.encode())


if __name__ == "__main__":
    sys.argv
    # shop = ShopServer(sys.argv[1])
    shop = ShopServer("C:\\Studies\\Final_Project\\server\\db.csv")
    while True:
        shop.start_connection()
