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
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.vars = locals()


class Tree:

    def __init__(self) -> None:
        self.root: Optional[Node] = None

    def _print_tree(
        self, node: Node, lst_return: list[dict[str, str | int]]
    ) -> list[dict[str, str | int]]:
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
        if node.left:
            self._print_tree(node.left, lst_return)
        if node.right:
            self._print_tree(node.right, lst_return)
        return lst_return

    def print_tree(self) -> str | None:
        if self.root:
            to_str = self._print_tree(self.root, [])
            place = 1
            to_send: str = ""
            for diction in to_str:
                x = ""
                for item in list(diction.items()):
                    x += f"{item[0]} = {str(item[1])} "
                to_send += f"{place}. {x}\n"
                place += 1
            return to_send

    def add_node(self, node: Node, search: str) -> None:
        if not self.root:
            self.root = node
        else:
            temp = self.root
            while temp:
                if temp.vars[search] >= node.vars[search]:
                    if not temp.left:
                        temp.left = node
                        break
                    else:
                        temp = temp.left
                else:
                    if not temp.right:
                        temp.right = node
                        break
                    temp = temp.right

    def _max_node(self, node: Node) -> Node:
        if not node.right:
            return node
        return self._max_node(node.right)

    def max_node(self) -> object:
        if self.root:
            return self._max_node(self.root)

    def remove_node(self, find: int | str, search: str) -> bool:
        temp: Optional[Node | None] = self.root
        if temp is not None:
            prev: Node = temp
            while temp:
                if find < temp.vars[search]:
                    if not temp.left:
                        return False
                    prev = temp
                    temp = temp.left
                    continue
                elif find > temp.vars[search]:
                    if not temp.right:
                        return False
                    prev = temp
                    temp = temp.right
                    continue
                else:
                    if not temp.left and not temp.right:
                        if prev.left is temp:
                            prev.left = None
                        elif prev.right is temp:
                            prev.right = None
                        else:
                            self.root = None
                    elif temp.left and not temp.right:
                        if prev.left is temp:
                            prev.left = None
                        elif prev.right is temp:
                            prev.right = None
                        else:
                            self.root = temp.left
                    elif not temp.left and temp.right:
                        if prev.left is temp:
                            prev.left = temp.right
                        elif prev.right is temp:
                            prev.right = temp.right
                        else:
                            self.root = temp.right
                    else:
                        if temp.left:
                            max_node = self._max_node(temp.left)
                            temp.vars[search] = max_node.vars[search]
                            max_node.vars[search] = find
                        prev = temp
                        temp = temp.left
                        continue
                return True
        # Empty Tree
        return False

    def _find_node_rec(
        self, find: int | str, node: Optional[Node], search: str
    ) -> Node | None:
        if node is None or find == node.vars[search]:
            return node
        elif find > node.vars[search]:
            return self._find_node_rec(find, node.right, search)
        elif find < node.vars[search]:
            return self._find_node_rec(find, node.left, search)

    def find_node_recursive(self, find: int | str, search: str) -> Node | None:
        node: Node | None = self._find_node_rec(find, self.root, search=search)
        return node if node else None

    def _count_nodes(self, node: Node | None, t: int = 1) -> int:
        if not node:
            return 0
        if node.left:
            t = self._count_nodes(node.left, t + 1)
        if node.right:
            t = self._count_nodes(node.right, t + 1)
        return t

    def count_nodes(self) -> int:
        return self._count_nodes(self.root)
