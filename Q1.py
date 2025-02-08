class Node:
    def __init__(self, key, color=True):
        self.key = key
        self.color = color  # True para vermelho, False para preto
        self.parent = None
        self.left = None
        self.right = None

class RedBlackTree:
    def __init__(self):
        self.NIL = Node(None, color=False)
        self.root = self.NIL

    def insert(self, key):
        new_node = Node(key)
        new_node.left = self.NIL
        new_node.right = self.NIL
        new_node.parent = self.NIL

        current = self.root
        parent = self.NIL
        while current != self.NIL:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent
        if parent == self.NIL:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self.insert_fixup(new_node)

    def insert_fixup(self, node):
        while node.parent.color == True:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == True:
                    node.parent.color = False
                    uncle.color = False
                    node.parent.parent.color = True
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = False
                    node.parent.parent.color = True
                    self.right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == True:
                    node.parent.color = False
                    uncle.color = False
                    node.parent.parent.color = True
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = False
                    node.parent.parent.color = True
                    self.left_rotate(node.parent.parent)
            if node == self.root:
                break
        self.root.color = False

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def delete(self, key):
        node = self.search(key)
        if node == self.NIL:
            return

        y = node
        y_original_color = y.color
        if node.left == self.NIL:
            x = node.right
            self.transplant(node, node.right)
        elif node.right == self.NIL:
            x = node.left
            self.transplant(node, node.left)
        else:
            y = self.minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self.transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color

        if y_original_color == False:
            self.delete_fixup(x)

    def transplant(self, u, v):
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def search(self, key):
        current = self.root
        while current != self.NIL and current.key != key:
            if key < current.key:
                current = current.left
            else:
                current = current.right
        return current

    def delete_fixup(self, x):
        while x != self.root and x.color == False:
            if x == x.parent.left:
                sibling = x.parent.right
                if sibling.color == True:
                    sibling.color = False
                    x.parent.color = True
                    self.left_rotate(x.parent)
                    sibling = x.parent.right
                if sibling.left.color == False and sibling.right.color == False:
                    sibling.color = True
                    x = x.parent
                else:
                    if sibling.right.color == False:
                        sibling.left.color = False
                        sibling.color = True
                        self.right_rotate(sibling)
                        sibling = x.parent.right
                    sibling.color = x.parent.color
                    x.parent.color = False
                    sibling.right.color = False
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                sibling = x.parent.left
                if sibling.color == True:
                    sibling.color = False
                    x.parent.color = True
                    self.right_rotate(x.parent)
                    sibling = x.parent.left
                if sibling.right.color == False and sibling.left.color == False:
                    sibling.color = True
                    x = x.parent
                else:
                    if sibling.left.color == False:
                        sibling.right.color = False
                        sibling.color = True
                        self.left_rotate(sibling)
                        sibling = x.parent.left
                    sibling.color = x.parent.color
                    x.parent.color = False
                    sibling.left.color = False
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = False

    def print_tree(self):
        self._print_tree(self.root, "", True)

    def _print_tree(self, node, indent, last):
        if node != self.NIL:
            print(indent, end='')
            if last:
                print("R---- ", end='')
                indent += "     "
            else:
                print("L---- ", end='')
                indent += "|    "
            color = "RED" if node.color else "BLACK"
            print(f"{node.key} ({color})")
            self._print_tree(node.left, indent, False)
            self._print_tree(node.right, indent, True)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return [item[0] for item in result]

    def _inorder(self, node, result):
        if node != self.NIL:
            self._inorder(node.left, result)
            result.append((node.key, 'Red' if node.color else 'Black'))
            self._inorder(node.right, result)

# Exemplo de uso
if __name__ == "__main__":
    rbt = RedBlackTree()
    keys = [5, 16, 22, 45, 2, 10, 18, 30, 50, 12, 1]
    for key in keys:
        rbt.insert(key)

    print("Árvore Rubro-Negra após inserções:")
    rbt.print_tree()
    print("\nInorder traversal:", rbt.inorder())
    print("--------------------------------------------")

    # # Remover alguns nós
    # rbt.delete(30)
    # rbt.delete(10)
    # rbt.delete(22)

    # print("\nÁrvore Rubro-Negra após remoções:")
    # rbt.print_tree()
    # print("--------------------------------------------")

    # rbt.insert(25)
    # rbt.insert(9)
    # rbt.insert(33)
    # rbt.insert(50)

    # print("\nÁrvore Rubro-Negra após inserções:")
    # rbt.print_tree()



   