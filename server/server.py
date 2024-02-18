import socket
from threading import Lock, Thread
import sys
from validate import Validate
from tree import Tree, Node
from datetime import date


class ShopServer:
    """
    server for customer debts
    you have to run instance.start_connection as main loop to receive
    """

    clients: list[socket.socket] = []
    MUTEX = Lock()

    def __init__(self, file_path: str, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port

        # starting server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
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
        """
        get customer properties like [parameter, value] and check all values than
        returns errors if exist or the value "true" in the first index and than all the details
        """
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
        """
        get properties after identity check and than check if name and last name exist
        and than updating the customer and adding line to csv file
        """
        error = ""
        if new_details[0].capitalize() != customer.name:
            error += f"did you mean {customer.name}"
        if new_details[1].capitalize() != customer.last_name:
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
        """
        after customer exist and fit updating the Node of the customer
        than replace the Node in the tree of dept and date
        """
        customer.dept = customer.dept + int(new_details[5])
        customer.date = self.s_date_to_date(new_details[4])
        customer.vars["dept"] = customer.dept
        customer.vars["date"] = customer.date
        if not start:  # because date didn't created first
            self.tree_by_dept.remove_node(customer, customer.dept)
            self.tree_by_date.remove_node(customer, customer.date)
            customer.left["dept"] = None
            customer.right["dept"] = None
            customer.left["date"] = None
            customer.right["date"] = None
            self.tree_by_dept.add_node(customer)
            self.tree_by_date.add_node(customer)

    def s_date_to_date(self, str_date: str) -> date:
        """converts string of date to date object"""
        sep = ""
        for l in str_date:
            if not l.isalpha() and not l.isdigit():
                sep = l
                break
        dates = [int(d) for d in str_date.split(sep)]
        day, month, year = dates
        return date(year, month, day)

    def add_line_to_file(self, customer_details: list[str]) -> None:
        """
        getting details of customer with no parameters and adding to the last line in the file
        """
        with open(self.file_path, "a+", encoding="UTF-8") as fw:
            fw.write(
                f"{customer_details[0].capitalize()},{customer_details[1].capitalize()},{int(customer_details[2])},{int(customer_details[3])},{customer_details[4]},{int(customer_details[5])}\n"
            )

    def set_new_customer(self, customer_details: list[str]) -> None:
        """
        ONLY NEW CUSTOMER
        adding the details of the customers into all the trees
        """
        customer = Node(
            customer_details[0].capitalize(),
            customer_details[1].capitalize(),
            customer_details[2],
            customer_details[3],
            self.s_date_to_date(customer_details[4]),
            int(customer_details[5]),
        )
        for t in self.trees.keys():
            self.trees[t].add_node(customer)
        self.add_line_to_file(customer_details)

    def start_connection(self) -> None:
        """the main running that open connection per client"""
        while True:
            try:
                cli_sock, cli_add = self.server_socket.accept()
            except ConnectionResetError:
                break
            except OSError:
                break
            else:
                print(f"Client {cli_add} connected")
                self.clients.append(cli_sock)
                Thread(
                    target=self.connection_handle, args=(cli_sock, cli_add), daemon=True
                ).start()

    def csv_import(self, binary_tree: Tree, orderby: str) -> bool:
        """when the server is start read from file the data into one tree"""
        print(f"csv importing to {orderby}")
        try:
            customers = self.open_file()
        except FileNotFoundError:
            print("FileNotFound")
            return False
        if customers == [["empty"]]:
            return False  # in case that there is no values
        for customer in customers:
            exist = self.tree_by_id.find_node_recursive(customer[2])
            if exist:
                self.customer_update(customer, exist, True)
                continue
            binary_tree.add_node(
                Node(
                    customer[0],
                    customer[1],
                    customer[2],
                    customer[3],
                    self.s_date_to_date(customer[4]),
                    int(customer[5]),
                )
            )
        return True

    def tree_to_tree(self) -> None:
        """
        calling csv by function and than create the ways of the trees into the nodes
        """
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

    def fix_file(self, all: list[str]) -> None:
        """before reading the file remove all empty lines"""
        empty = 0
        for a in all:
            if a == "":
                empty += 1
        for _ in range(empty):
            all.remove("")
        with open(self.file_path, "w+", encoding="UTF-8") as csv:  # encoding for hebrew
            for a in all:
                csv.write(a + "\n")

    def open_file(self) -> list[list[str]]:
        """open the file and calling by instance.csv_import"""
        with open(self.file_path, "r", encoding="UTF-8") as csv:  # encoding for hebrew
            non_ordered_data: list[str] = csv.read().split("\n")
            if "" in non_ordered_data:
                self.fix_file(non_ordered_data)
                if "" in non_ordered_data:
                    return [["empty"]]
            data: list[list[str]] = [
                self.customer_str_to_list(customer) for customer in non_ordered_data
            ]
            return data

    def customer_str_to_list(self, customer: str) -> list[str]:
        """
        call by open_file and for reading the file and ordering the values for the nodes
        """
        customer_lst: list[str] = customer.split(",")
        fn: str = customer_lst[0]
        ln: str = customer_lst[1]
        identity: str = self.zero_add(customer_lst[2], 9)
        phn: str = "0" + customer_lst[3]
        dt: str = customer_lst[4]
        dp: str = customer_lst[5]
        return [fn, ln, identity, phn, dt, dp]

    def zero_add(self, val: str, length: int) -> str:
        """filling the value with zero from the left"""
        while len(val) != length:
            val = "0" + val
        return val

    def operate(self, mess: str) -> str | None:
        """return the operator"""
        if "!=" in mess:
            return "!="
        elif "<" in mess:
            return "<"
        elif ">" in mess:
            return ">"
        elif "=" in mess:
            return "="
        return None

    def trimer(self, word: str) -> str:
        """trim white space from left and right and also return words with one space"""
        return " ".join(word.split())

    def send_to_client(self, client_socket: socket.socket, message: str) -> None:
        """used to send message and than string to tell the client to stop"""
        client_socket.sendall(message.encode())
        client_socket.sendall("&%^$*$(#)@!".encode())

    def connection_handle(
        self, client_socket: socket.socket, client_address: tuple[str, int]
    ) -> None:
        """for each customer it is the main server"""
        while True:
            try:
                message = client_socket.recv(1024).decode("UTF-8")
            except ConnectionResetError:
                print(f"{client_address} shuted off")
                self.clients.remove(client_socket)
                break

            if message.startswith("set"):
                message = message[4:]
                valid: list[str] = self.validation(message)
                if valid[0] != "true":
                    self.send_to_client(client_socket, valid[0])
                    continue
                valid = valid[1:]  # cut the 'true'
                customer_exist = self.tree_by_id.find_node_recursive(valid[2])
                with self.MUTEX:
                    if customer_exist:
                        resp = self.customer_exist_update(valid, customer_exist)
                        self.send_to_client(client_socket, resp)
                        continue
                    self.set_new_customer(valid)
                    self.send_to_client(client_socket, "customer successfully added.")

            elif message.startswith("print"):
                message = message.split()
                if len(message) == 2:
                    all_customers = self.trees[message[1]].print_tree()
                else:
                    all_customers = self.tree_by_dept.print_tree()
                if all_customers:
                    self.send_to_client(client_socket, all_customers)
                else:
                    self.send_to_client(client_socket, "No Customers")

            elif message.startswith("goodbye"):
                self.server_socket.close()
                print("Server shuting off")

            elif message.startswith("select"):
                message = message[7:]
                operate: str | None = self.operate(message)
                if not operate:
                    self.send_to_client(client_socket, "Operator not found!")
                    continue
                message = message.split(operate)
                message = [self.trimer(w) for w in message]
                all_customers = self.trees[message[0].lower()].select_from(
                    message[1], operate
                )
                self.send_to_client(client_socket, all_customers)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        shop = ShopServer(sys.argv[1], "127.0.0.1", 34500)
    else:
        shop = ShopServer(
            "C:\\Studies\\Final_Project\\server\\db.csv", "127.0.0.1", 34500
        )
    t = Thread(target=shop.start_connection)
    t.start()
    t.join()
