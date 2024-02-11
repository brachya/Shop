from typing import Optional


class Node:
    def __init__(
        self,
        name: str,
        last_name: str,
        identity: int,
        phone: int,
        date: str,
        dept: int,
    ) -> None:
        self.name = name
        self.last_name = last_name
        self.identity = identity
        self.phone = phone
        self.date = date
        self.dept = dept
        self.left: dict[str, Node | None] = {
            "name": None,
            "last_name": None,
            "identity": None,
            "phone": None,
            "date": None,
            "dept": None,
        }
        self.right: dict[str, Node | None] = {
            "name": None,
            "last_name": None,
            "identity": None,
            "phone": None,
            "date": None,
            "dept": None,
        }
        self.vars = locals()

    def __str__(self) -> str:
        return f"{self.name} {self.last_name} {self.identity} {self.phone} {self.date} {self.dept}"


class Tree:

    def __init__(self) -> None:
        self.root: Optional[Node] = None

    def _print_tree(
        self, node: Node, lst_return: list[dict[str, str | int]], orderby: str
    ) -> None:
        if not node:
            return
        if node.left[orderby]:
            self._print_tree(node.left[orderby], lst_return, orderby)  # type: ignore
        lst_return.append(
            {
                "first name": node.name,
                "last name": node.last_name,
                "id": node.identity,
                "phone": node.phone,
                "date": node.date,
                "dept": node.dept,
            }
        )
        if node.right[orderby]:
            self._print_tree(node.right[orderby], lst_return, orderby)  # type: ignore

    def print_tree(self, orderby: str) -> str | None:
        if self.root:
            to_str: list[dict[str, str | int]] = []
            self._print_tree(self.root, to_str, orderby)
            place = 1
            to_send: str = ""
            for diction in to_str:
                x = ""
                for item in list(diction.items()):
                    x += f"{item[0]} = {str(item[1])} "
                to_send += f"{place}. {x}\n"
                place += 1
            return to_send

    def add_node(self, node: Node, orderby: str) -> None:
        if not self.root:
            self.root = node
        else:
            temp = self.root
            while temp:
                if node.vars[orderby] <= temp.vars[orderby]:
                    if not temp.left[orderby]:
                        temp.left[orderby] = node
                        break
                    temp = temp.left[orderby]
                else:
                    if not temp.right[orderby]:
                        temp.right[orderby] = node
                        break
                    temp = temp.right[orderby]

    def _max_node(self, node: Node, orderby: str) -> Node:
        if not node.right[orderby]:
            return node
        return self._max_node(node.right[orderby], orderby)  # type: ignore

    def max_node(self, orderby: str) -> object:
        if self.root:
            return self._max_node(self.root, orderby)

    def remove_node(self, find: int | str, orderby: str) -> bool:
        temp: Optional[Node | None] = self.root
        if temp is not None:
            prev: Node = temp
            while temp:
                if find < temp.vars[orderby]:
                    if temp.left[orderby] is None:
                        return False
                    prev = temp
                    temp = temp.left[orderby]
                    continue
                elif find > temp.vars[orderby]:
                    if not temp.right[orderby]:
                        return False
                    prev = temp
                    temp = temp.right[orderby]
                    continue
                else:
                    if not temp.left[orderby] and not temp.right[orderby]:
                        if prev.left[orderby] is temp:
                            prev.left[orderby] = None
                        elif prev.right[orderby] is temp:
                            prev.right[orderby] = None
                        else:
                            self.root = None
                    elif temp.left[orderby] and not temp.right[orderby]:
                        if prev.left[orderby] is temp:
                            prev.left[orderby] = None
                        elif prev.right[orderby] is temp:
                            prev.right[orderby] = None
                        else:
                            self.root = temp.left[orderby]
                    elif not temp.left[orderby] and temp.right[orderby]:
                        if prev.left[orderby] is temp:
                            prev.left[orderby] = temp.right[orderby]
                        elif prev.right[orderby] is temp:
                            prev.right[orderby] = temp.right[orderby]
                        else:
                            self.root = temp.right[orderby]
                    else:
                        if temp.left[orderby]:
                            max_node = self._max_node(temp.left[orderby], orderby)  # type: ignore
                            temp.vars[orderby] = max_node.vars[orderby]
                            max_node.vars[orderby] = find
                        prev = temp
                        temp = temp.left[orderby]
                        continue
                return True
        # Empty Tree
        return False

    def _find_node_rec(
        self, find: int | str, node: Optional[Node], orderby: str
    ) -> Node | None:
        if node is None or find == node.vars[orderby]:
            return node
        elif find > node.vars[orderby]:
            return self._find_node_rec(find, node.right[orderby], orderby)
        elif find < node.vars[orderby]:
            return self._find_node_rec(find, node.left[orderby], orderby)

    def find_node_recursive(self, find: int | str, orderby: str) -> Node | None:
        node: Node | None = self._find_node_rec(find, self.root, orderby=orderby)
        return node if node else None

    def _count_nodes(self, node: Node | None, orderby: str, t: int = 1) -> int:
        if not node:
            return 0
        if node.left[orderby]:
            t = self._count_nodes(node.left[orderby], orderby, t + 1)
        if node.right[orderby]:
            t = self._count_nodes(node.right[orderby], orderby, t + 1)
        return t

    def count_nodes(self, orderby: str) -> int:
        return self._count_nodes(self.root, orderby)
