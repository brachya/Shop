from typing import Optional


class Node:
    def __init__(
        self,
        name: str,
        last_name: str,
        identity: str,
        phone: str,
        date: str,
        dept: str,
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
        self.vars: dict[str, str] = locals()

    def __str__(self) -> str:
        return f"{self.name} {self.last_name} {self.identity} {self.phone} {self.date} {self.dept}"

    @property
    def to_dict(self) -> dict[str, str]:
        return {
            "first name": self.name,
            "last name": self.last_name,
            "id": self.identity,
            "phone": self.phone,
            "date": self.date,
            "dept": self.dept,
        }

    # def vars_reset(self) -> None:
    #     self.vars = locals()


class Tree:

    def __init__(self, orderby: str) -> None:
        self.root: Optional[Node] = None
        self.orderby: str = orderby

    def _nodes(self, node: Optional[Node], lst_return: list[Node]) -> None:
        if not node:
            return
        if node.left[self.orderby]:
            self._nodes(node.left[self.orderby], lst_return)
        lst_return.append(node)
        if node.right[self.orderby]:
            self._nodes(node.right[self.orderby], lst_return)

    def nodes(self) -> list[Node]:
        lst_return: list[Node] = []
        if self.root:
            self._nodes(self.root, lst_return)
        return lst_return

    def _print_tree(
        self, node: Optional[Node], lst_return: list[dict[str, str]]
    ) -> None:
        if not node:
            return
        if node.left[self.orderby]:
            self._print_tree(node.left[self.orderby], lst_return)
        lst_return.append(node.to_dict)
        if node.right[self.orderby]:
            self._print_tree(node.right[self.orderby], lst_return)

    def print_tree(self) -> str | None:
        if self.root:
            to_str: list[dict[str, str]] = []
            self._print_tree(self.root, to_str)
            place = 1
            to_send: str = ""
            for diction in to_str:
                x = ""
                for item in list(diction.items()):
                    x += f"{item[0]} = {str(item[1])} "
                to_send += f"{place}. {x}\n"
                place += 1
            return to_send

    def _select_equal(
        self, value: str, node: Optional[Node], lst_return: list[dict[str, str]]
    ) -> None:
        if not node:
            return
        if value == node.vars[self.orderby]:
            lst_return.append(node.to_dict)
        if value > node.vars[self.orderby]:
            if node.right[self.orderby]:
                self._select_equal(value, node.right[self.orderby], lst_return)
        else:
            if node.left[self.orderby]:
                self._select_equal(value, node.left[self.orderby], lst_return)

    def _select_non_equal(
        self, value: str, node: Optional[Node], lst_return: list[dict[str, str]]
    ) -> None:
        if not node:
            return
        if node.left[self.orderby]:
            self._select_non_equal(value, node.left[self.orderby], lst_return)
        if value != node.vars[self.orderby]:
            lst_return.append(node.to_dict)
        if node.right[self.orderby]:
            self._select_non_equal(value, node.right[self.orderby], lst_return)

    def _select_above(
        self,
        value: str,
        node: Optional[Node],
        lst_return: list[dict[str, str]],
        exist: bool = False,
    ) -> None:
        if not node:
            return
        if not exist:
            if node.vars[self.orderby] < value:
                if node.right[self.orderby]:

                    self._select_above(
                        value, node.right[self.orderby], lst_return, exist
                    )
            elif node.vars[self.orderby] > value:
                if node.left[self.orderby]:
                    self._select_above(
                        value, node.left[self.orderby], lst_return, exist
                    )
                lst_return.append(node.to_dict)
                if node.right[self.orderby]:
                    self._select_above(
                        value, node.right[self.orderby], lst_return, True
                    )
            else:
                if node.right[self.orderby]:
                    self._select_above(
                        value, node.right[self.orderby], lst_return, True
                    )
        else:
            if node.left[self.orderby]:
                self._select_above(value, node.left[self.orderby], lst_return, exist)
            lst_return.append(node.to_dict)
            if node.right[self.orderby]:
                self._select_above(value, node.right[self.orderby], lst_return, exist)

    def _select_under(
        self, value: str, node: Optional[Node], lst_return: list[dict[str, str]]
    ) -> None:
        if not node:
            return
        if node.left[self.orderby]:
            self._select_under(value, node.left[self.orderby], lst_return)
        if node.vars[self.orderby] < value:
            lst_return.append(node.to_dict)
            if node.right[self.orderby]:
                self._select_under(value, node.right[self.orderby], lst_return)

    def select_from(self, value: str, operate: str) -> str:
        found: list[dict[str, str]] = []
        if operate == ">":
            self._select_above(value, self.root, found)
        elif operate == "<":
            self._select_under(value, self.root, found)
        elif operate == "=":
            self._select_equal(value, self.root, found)
        else:
            self._select_non_equal(value, self.root, found)
        if not found:
            return "No values"
        place = 1
        to_send: str = ""
        for diction in found:
            x = ""
            for item in list(diction.items()):
                x += f"{item[0]} = {str(item[1])} "
            to_send += f"{place}. {x}\n"
            place += 1
        return to_send

    def add_node(self, node: Node) -> None:
        if not self.root:
            self.root = node
        else:
            temp = self.root
            while temp:
                if node.vars[self.orderby] <= temp.vars[self.orderby]:
                    if not temp.left[self.orderby]:
                        temp.left[self.orderby] = node
                        break
                    temp = temp.left[self.orderby]
                else:
                    if not temp.right[self.orderby]:
                        temp.right[self.orderby] = node
                        break
                    temp = temp.right[self.orderby]

    def _max_node(self, node: Node) -> Node:
        if not node.right[self.orderby]:
            return node
        return self._max_node(node.right[self.orderby])  # type: ignore

    def max_node(self) -> object:
        if self.root:
            return self._max_node(self.root)

    def remove_node(self, node: Node, find: str) -> bool:
        temp: Optional[Node | None] = self.root
        if temp is not None:
            prev: Node = temp
            while temp:
                if find < temp.vars[self.orderby]:
                    if temp.left[self.orderby] is None:
                        return False
                    prev = temp
                    temp = temp.left[self.orderby]
                    continue
                elif find > temp.vars[self.orderby]:
                    if not temp.right[self.orderby]:
                        return False
                    prev = temp
                    temp = temp.right[self.orderby]
                    continue
                else:
                    if temp is not node:
                        prev = temp
                        temp = temp.left[self.orderby]
                        continue
                    if not temp.left[self.orderby] and not temp.right[self.orderby]:
                        if prev.left[self.orderby] is temp:
                            prev.left[self.orderby] = None
                        elif prev.right[self.orderby] is temp:
                            prev.right[self.orderby] = None
                        else:
                            self.root = None
                    elif temp.left[self.orderby] and not temp.right[self.orderby]:
                        if prev.left[self.orderby] is temp:
                            prev.left[self.orderby] = None
                        elif prev.right[self.orderby] is temp:
                            prev.right[self.orderby] = None
                        else:
                            self.root = temp.left[self.orderby]
                    elif not temp.left[self.orderby] and temp.right[self.orderby]:
                        if prev.left[self.orderby] is temp:
                            prev.left[self.orderby] = temp.right[self.orderby]
                        elif prev.right[self.orderby] is temp:
                            prev.right[self.orderby] = temp.right[self.orderby]
                        else:
                            self.root = temp.right[self.orderby]
                    else:
                        if temp.left[self.orderby]:
                            max_node = self._max_node(temp.left[self.orderby])  # type: ignore
                            temp.vars[self.orderby] = max_node.vars[self.orderby]
                            max_node.vars[self.orderby] = find
                        prev = temp
                        temp = temp.left[self.orderby]
                        continue
                return True
        # Empty Tree
        return False

    def _find_node_rec(
        self, find: str, node: Optional[Node], orderby: str
    ) -> Node | None:
        if node is None or find == node.vars[orderby]:
            return node
        elif find > node.vars[orderby]:
            return self._find_node_rec(find, node.right[orderby], orderby)
        elif find < node.vars[orderby]:
            return self._find_node_rec(find, node.left[orderby], orderby)

    def find_node_recursive(self, find: str) -> Node | None:
        node: Node | None = self._find_node_rec(find, self.root, self.orderby)
        return node if node else None

    def _count_nodes(self, node: Node | None, t: int = 1) -> int:
        if not node:
            return 0
        if node.left[self.orderby]:
            t = self._count_nodes(node.left[self.orderby], t + 1)
        if node.right[self.orderby]:
            t = self._count_nodes(node.right[self.orderby], t + 1)
        return t

    def count_nodes(self) -> int:
        return self._count_nodes(self.root)
