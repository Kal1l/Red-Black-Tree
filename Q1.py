class Node:
    def __init__(self, data, color="R"):
        self.data = data
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(0)
        self.TNULL.color = "B"
        self.root = self.TNULL
        self.insertion_order = []

    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.data = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = "R"

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = "B"
            self.insertion_order.append(key)  
            return

        if node.parent.parent == None:
            self.insertion_order.append(key) 
            return

        self.fix_insert(node)
        self.insertion_order.append(key) 

    def fix_insert(self, k):
        while k.parent.color == "R":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == "R":
                    u.color = "B"
                    k.parent.color = "B"
                    k.parent.parent.color = "R"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = "B"
                    k.parent.parent.color = "R"
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == "R":
                    u.color = "B"
                    k.parent.color = "B"
                    k.parent.parent.color = "R"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = "B"
                    k.parent.parent.color = "R"
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "B"

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
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
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.data == key:
                z = node

            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print("Couldn't find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == "B":
            self.fix_delete(x)

    def rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def fix_delete(self, x):
        while x != self.root and x.color == "B":
            if x == x.parent.left:
                s = x.parent.right
                if s.color == "R":
                    s.color = "B"
                    x.parent.color = "R"
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == "B" and s.right.color == "B":
                    s.color = "R"
                    x = x.parent
                else:
                    if s.right.color == "B":
                        s.left.color = "B"
                        s.color = "R"
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = "B"
                    s.right.color = "B"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == "R":
                    s.color = "B"
                    x.parent.color = "R"
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == "B" and s.right.color == "B":
                    s.color = "R"
                    x = x.parent
                else:
                    if s.left.color == "B":
                        s.right.color = "B"
                        s.color = "R"
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = "B"
                    s.left.color = "B"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "B"

    def deleteByVal(self, data):
        self.delete_node_helper(self.root, data)
        if data in self.insertion_order:
            self.insertion_order.remove(data)

    def printInOrder(self):
        for key in self.insertion_order:
            print(key, end=" ")
        print()

    def find(self, key):
        return self.search_tree_helper(self.root, key)

    def search_tree_helper(self, node, key):
        if node == self.TNULL or key == node.data:
            return node

        if key < node.data:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    def findMin(self):
        return self.minimum(self.root).data

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def findMax(self):
        return self.maximum(self.root).data

    def maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node

    def findKth(self, k):
        return self.find_kth_helper(self.root, k)

    def find_kth_helper(self, node, k):
        stack = []
        while True:
            while node != self.TNULL:
                stack.append(node)
                node = node.left
            node = stack.pop()
            k -= 1
            if k == 0:
                return node.data
            node = node.right

    def findInterval(self, low, high):
        self.find_interval_helper(self.root, low, high)

    def find_interval_helper(self, node, low, high):
        if node == self.TNULL:
            return
        if low < node.data:
            self.find_interval_helper(node.left, low, high)
        if low <= node.data <= high:
            print(node.data, end=" ")
        if high > node.data:
            self.find_interval_helper(node.right, low, high)

    def printTree(self):
        self.print_tree_helper(self.root, "", True)

    def print_tree_helper(self, node, indent, last):
        if node != self.TNULL:
            print(indent, end="")
            if last:
                print("R----", end="")
                indent += "     "
            else:
                print("L----", end="")
                indent += "|    "

            s_color = "R" if node.color == "R" else "B"
            print(str(node.data) + "(" + s_color + ")")
            self.print_tree_helper(node.left, indent, False)
            self.print_tree_helper(node.right, indent, True)

if __name__ == "__main__":
    bst = RedBlackTree()

    # Questão 6 - Operações
    keys_to_insert = [5, 16, 22, 45, 2, 10, 18, 30, 50, 12, 1]
    for key in keys_to_insert:
        bst.insert(key)

    print("Árvore em ordem de inserção:")
    bst.printInOrder()
    print("\nÁrvore após inserções:")
    bst.printTree()

    print("\nProcurando pelas chaves 22 e 15:")
    print(bst.find(22).data if bst.find(22) != bst.TNULL else "Não encontrado")
    print(bst.find(15).data if bst.find(15) != bst.TNULL else "Não encontrado")

    keys_to_delete = [30, 10, 22]
    for key in keys_to_delete:
        bst.deleteByVal(key)
    print("\nÁrvore após exclusões:")
    bst.printTree()
    keys_to_insert = [25, 9, 33, 50]
    for key in keys_to_insert:
        bst.insert(key)
    bst.printInOrder()    
    print("\nÁrvore novas inserções:")
    bst.printTree()

    print("\nMaior valor:", bst.findMax())
    print("Menor valor:", bst.findMin())
    print("Quinto menor valor:", bst.findKth(5))

    print("\nElementos entre 10 e 30:")
    bst.findInterval(10, 30)