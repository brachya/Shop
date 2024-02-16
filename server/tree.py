from typing import Optional, Union


class Node:
    """this node hold the customer properties"""

    def __init__(
        self,
        name: str,
        last_name: str,
        identity: str,
        phone: str,
        date: str,
        dept: int,
    ) -> None:
        self.name = name
        self.last_name = last_name
        self.identity = identity
        self.phone = phone
        self.date = date
        self.dept: int = dept
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
        self.vars: dict[str, Union[str, int]] = locals()

    def __str__(self) -> str:
        return f"{self.name} {self.last_name} {self.identity} {self.phone} {self.date} {self.dept}"

    @property
    def to_dict(self) -> dict[str, str]:
        """take the values of the customer and return in dictionary"""
        return {
            "first name": self.name,
            "last name": self.last_name,
            "id": self.identity,
            "phone": self.phone,
            "date": self.date,
            "dept": str(self.dept),
        }


class Tree:
    """binary tree that can work on multiply ways and work by the
    orderby that has to be exactly the same as the variable of the node,
    IMPORTANT: the tree works by equal to left"""

    def __init__(self, orderby: str) -> None:
        self.root: Optional[Node] = None
        self.orderby: str = orderby

    def _nodes(self, node: Optional[Node], lst_return: list[Node]) -> None:
        """add all nodes from node, into list to copy the tree"""
        if not node:
            return
        if node.left[self.orderby]:
            self._nodes(node.left[self.orderby], lst_return)
        lst_return.append(node)
        if node.right[self.orderby]:
            self._nodes(node.right[self.orderby], lst_return)

    def nodes(self) -> list[Node]:
        """call _nodes from the root"""
        lst_return: list[Node] = []
        if self.root:
            self._nodes(self.root, lst_return)
        return lst_return

    def _print_tree(
        self, node: Optional[Node], lst_return: list[dict[str, str]]
    ) -> None:
        """adding all the node from node, as dictionary to print"""
        if not node:
            return
        if node.left[self.orderby]:
            self._print_tree(node.left[self.orderby], lst_return)
        lst_return.append(node.to_dict)
        if node.right[self.orderby]:
            self._print_tree(node.right[self.orderby], lst_return)

    def print_tree(self) -> str | None:
        """calling _print_tree from the root and converting the dictionary to string"""
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
        """adding to list all the equal values from node, (if node is dept so converting the value to int)"""
        if not node:
            return
        if type(node.vars[self.orderby]) == int:
            value = int(value)  # type: ignore
        if value == node.vars[self.orderby]:
            lst_return.append(node.to_dict)
        if value > node.vars[self.orderby]:  # type: ignore
            if node.right[self.orderby]:
                self._select_equal(value, node.right[self.orderby], lst_return)
        else:
            if node.left[self.orderby]:
                self._select_equal(value, node.left[self.orderby], lst_return)

    def _select_non_equal(
        self, value: str, node: Optional[Node], lst_return: list[dict[str, str]]
    ) -> None:
        """adding to list all the non equal values from node, (if node is dept so converting the value to int)"""
        if not node:
            return
        if type(node.vars[self.orderby]) == int:
            value = int(value)  # type: ignore
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
        """adding to list all the above values from node, (if node is dept so converting the value to int)"""
        if not node:
            return
        if type(node.vars[self.orderby]) == int:
            value = int(value)  # type: ignore
        if not exist:
            if node.vars[self.orderby] < value:  # type: ignore
                if node.right[self.orderby]:

                    self._select_above(
                        value, node.right[self.orderby], lst_return, exist
                    )
            elif node.vars[self.orderby] > value:  # type: ignore
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
        """adding to list all the low values from node, (if node is dept so converting the value to int)"""
        if not node:
            return
        if type(node.vars[self.orderby]) == int:
            value = int(value)  # type: ignore
        if node.left[self.orderby]:
            self._select_under(value, node.left[self.orderby], lst_return)
        if node.vars[self.orderby] < value:  # type: ignore
            lst_return.append(node.to_dict)
            if node.right[self.orderby]:
                self._select_under(value, node.right[self.orderby], lst_return)

    def select_from(self, value: str, operate: str) -> str:
        """calling functions from root to find the results and convert to string"""
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
        """adding node to tree by checking the way and finding empty way"""
        if not self.root:
            self.root = node
        else:
            temp = self.root
            while temp:
                if node.vars[self.orderby] <= temp.vars[self.orderby]:  # type: ignore
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
        """searching for the max node from the inserted node by return the right node before the empty node"""
        if not node.right[self.orderby]:
            return node
        return self._max_node(node.right[self.orderby])  # type: ignore

    def max_node(self) -> object:
        """calling _max_node with the root"""
        if self.root:
            return self._max_node(self.root)

    def remove_node(self, node: Node, find: str | int) -> bool:
        "searching for the node that equal the find value and cut the connection to him and from him"
        temp: Optional[Node | None] = self.root
        if temp is not None:
            prev: Node = temp
            while temp:
                if find < temp.vars[self.orderby]:  # type: ignore
                    if temp.left[self.orderby] is None:
                        return False
                    prev = temp
                    temp = temp.left[self.orderby]
                    continue
                elif find > temp.vars[self.orderby]:  # type: ignore
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
        """return the first node that match the value"""
        if orderby == "dept":
            find = int(find)  # type: ignore
        if node is None or find == node.vars[orderby]:
            return node
        elif find > node.vars[orderby]:  # type: ignore
            return self._find_node_rec(find, node.right[orderby], orderby)
        elif find < node.vars[orderby]:  # type: ignore
            return self._find_node_rec(find, node.left[orderby], orderby)

    def find_node_recursive(self, find: str) -> Node | None:
        """calling the _find_node_rec and with the root"""
        node: Node | None = self._find_node_rec(find, self.root, self.orderby)
        return node if node else None
