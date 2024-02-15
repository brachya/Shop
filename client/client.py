import socket
from threading import Thread


class Client:
    """
    client side that in receive until stop message,
    open 2 thread and the main thread is the send
    """

    def __init__(self, IP: str, PORT: int) -> None:
        self.__IP: str = IP
        self.__PORT: int = PORT
        self.client_socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.connection()
        t = Thread(target=self.receiving, daemon=True)
        t1 = Thread(target=self.sending)
        t.start()
        t1.start()
        t1.join()

    def connection(self):
        """at start ,search for server and if not exist can try again"""
        connected = False
        while not connected:
            try:
                self.client_socket.connect((self.__IP, self.__PORT))
                connected = True
            except ConnectionRefusedError:
                print("Server not found!")
                input("Click enter to try again.")

    def receiving(self) -> None:
        """the receiver that print message from server until get '&%^$*$(#)@!'"""
        while True:
            try:
                message: str = self.client_socket.recv(1024).decode()
                print(message, end="")
                while True:
                    message: str = self.client_socket.recv(1024).decode()
                    if message.endswith("&%^$*$(#)@!"):
                        print(message[:-11])
                        break
                    print(message, end="")
            except:
                break

    def key_check(self, keys: list[str], error: list[str]) -> None:
        """get list of parameter and validate that it is the correct values"""
        if keys[0] != "first name":
            error.append("did you mean first name")
        if keys[1] != "last name":
            error.append("did you mean last name")
        if keys[2] not in ["id", "identity"]:
            error.append("did you mean id")
        if keys[3] != "phone":
            error.append("did you mean phone")
        if keys[4] != "date":
            error.append("did you mean dept")
        if keys[5] != "dept":
            error.append("did you mean dept")

    def set_check(self, mess: str) -> list[str]:
        """checks the parameters in set command"""
        equation: int = mess.count("=")
        comma: int = mess.count(",")
        if equation != 6 or comma != 5:
            return ["false", f"missing {comma - 5} ',' or {equation - 6} '='."]
        checking = mess[4:].split(",")
        checking = [val.split("=") for val in checking]
        data = [prompt[1] for prompt in checking]
        data = [" ".join(p.split()) for p in data]
        checking = [prompt[0] for prompt in checking]
        checking = [" ".join(p.split()) for p in checking]
        error: list[str] = []
        self.key_check(checking, error)
        if error:
            return ["false", "\n".join(error)]
        message = ""
        for n in range(6):
            message += f",{checking[n]}={data[n]}"
        message = "set " + message[1:]
        return ["true", message]

    def select_check(self, mess: str) -> list[str]:
        """checks the parameters in select commands"""
        my_operator: str | None = self.my_operate_get(mess)
        if my_operator is None:
            return ["false", "No operator!"]
        checking = mess[7:].split(my_operator)
        data = self.trimer(checking[1])
        checking = self.trimer(checking[0])
        if checking not in [
            "first name",
            "last name",
            "identity",
            "phone",
            "date",
            "dept",
        ]:
            return ["false", "wrong parameter"]
        return ["true", f"select {checking} {my_operator} {data}"]

    def my_operate_get(self, mess: str) -> str | None:
        """find the operator return the operator"""
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
        """return string with no spaces in left or right but one between every words"""
        return " ".join(word.split())

    def sending(self) -> None:
        """the main loop to send the server the messages and close the program when send 'quit'"""
        while True:
            mess = input("==> ")
            check: list[str] = []
            if mess.startswith("set"):
                check = self.set_check(mess)
            elif mess.startswith("select"):
                check = self.select_check(mess)
            elif mess.startswith("print"):
                check = ["true"] + [mess]
            elif mess.startswith("quit") or mess.startswith("goodbye"):
                check = ["true"] + [mess]
            else:
                check = ["false"] + ["Command not available"]
            if check[0] == "false":
                print(check[1])
                continue
            mess = check[1]
            try:
                self.client_socket.sendall(mess.encode())
            except ConnectionResetError:
                print("500 server shuted off")
                break
            if mess == "quit" or mess == "goodbye":
                break


if __name__ == "__main__":
    cli = Client("127.0.0.1", 34500)
