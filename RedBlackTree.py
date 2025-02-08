from Node import Node

class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(0)
        self.TNULL.color = "P"
        self.root = self.TNULL
        self.insertion_order = []

    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.data = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = "V"

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
            node.color = "P"
            self.insertion_order.append(key)  
            return

        if node.parent.parent == None:
            self.insertion_order.append(key) 
            return

        self.fix_insert(node)
        self.insertion_order.append(key) 

    def fix_insert(self, k):
        while k.parent.color == "V":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == "V":
                    u.color = "P"
                    k.parent.color = "P"
                    k.parent.parent.color = "V"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = "P"
                    k.parent.parent.color = "V"
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == "V":
                    u.color = "P"
                    k.parent.color = "P"
                    k.parent.parent.color = "V"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = "P"
                    k.parent.parent.color = "V"
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "P"

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
        if y_original_color == "P":
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
        while x != self.root and x.color == "P":
            if x == x.parent.left:
                s = x.parent.right
                if s.color == "V":
                    s.color = "P"
                    x.parent.color = "V"
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == "P" and s.right.color == "P":
                    s.color = "V"
                    x = x.parent
                else:
                    if s.right.color == "P":
                        s.left.color = "P"
                        s.color = "V"
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = "P"
                    s.right.color = "P"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == "V":
                    s.color = "P"
                    x.parent.color = "V"
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == "P" and s.right.color == "P":
                    s.color = "V"
                    x = x.parent
                else:
                    if s.left.color == "P":
                        s.right.color = "P"
                        s.color = "V"
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = "P"
                    s.left.color = "P"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "P"

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
            if node == self.root:
                print("R----", end="")
                indent += "     "
            elif last:
                print("D----", end="")
                indent += "     "
            else:
                print("E----", end="")
                indent += "|    "

            s_color = "V" if node.color == "V" else "P"
            print(str(node.data) + "(" + s_color + ")")
            self.print_tree_helper(node.left, indent, False)
            self.print_tree_helper(node.right, indent, True)