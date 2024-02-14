import socket
from threading import Thread


class Client:

    def __init__(self, IP: str, PORT: int) -> None:
        self.__IP: str = IP
        self.__PORT: int = PORT

        self.client_socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.connection()

        Thread(target=self.receiving, daemon=True).start()
        Thread(target=self.sending).start()

    def connection(self):
        connected = False
        while not connected:
            try:
                self.client_socket.connect((self.__IP, self.__PORT))
                connected = True
            except ConnectionRefusedError:
                print("Server not found!")
                input("Click enter to try again.")

    def receiving(self) -> None:
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
        if keys[0] != "first name":
            error.append("did you mean first name")
        if keys[1] != "last name":
            error.append("did you mean last name")
        if keys[2] != "id":
            error.append("did you mean id")
        if keys[3] != "phone":
            error.append("did you mean phone")
        if keys[4] != "date":
            error.append("did you mean dept")
        if keys[5] != "dept":
            error.append("did you mean dept")

    def set_check(self, mess: str) -> list[str]:
        equation: int = mess.count("=")
        comma: int = mess.count(",")
        if equation != 6 or comma != 5:
            print(f"missing {comma - 5} ',' or {equation - 6} '='.")
            return ["false"]
        checking = mess[4:].split(",")
        checking = [val.split("=") for val in checking]
        data = [prompt[1] for prompt in checking]
        data = [" ".join(p.split()) for p in data]
        checking = [prompt[0] for prompt in checking]
        checking = [" ".join(p.split()) for p in checking]
        error: list[str] = []
        self.key_check(checking, error)
        if error:
            [print(warning) for warning in error]
            return ["false"]
        message = ""
        for n in range(6):
            message += f",{checking[n]}={data[n]}"
        message = "set " + message[1:]
        return ["true"] + [message]

    def select_check(self, mess: str) -> list[str]:
        operate = self.operate(mess)
        checking = mess[7:].split(operate)
        data = [prompt[1] for prompt in checking]
        data = [" ".join(p.split()) for p in data]
        checking = [prompt[0] for prompt in checking]
        checking = " ".join([" ".join(p.split()) for p in checking])
        if checking not in [
            "first name",
            "last name",
            "identity",
            "phone",
            "date",
            "dept",
        ]:
            print("wrong parameter")
            return ["false"]
        return ["true"] + [mess]

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
        return " ".join(word.split())

    def sending(self) -> None:
        while True:
            mess = input("==> ")
            check: list[str] = ["false"]
            if mess.startswith("set"):
                check = self.set_check(mess)
            elif mess.startswith("select"):
                check = self.select_check(mess)
            if check[0] == "false":
                continue
            mess = check[1]
            try:
                self.client_socket.sendall(mess.encode())
            except ConnectionResetError:
                print("500 server shuted off")
                break
            if mess == "bye" or mess == "goodbye":
                break


if __name__ == "__main__":
    cli = Client("127.0.0.1", 34500)
