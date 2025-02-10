class Node:
    def __init__(self, data, color="V"):
        self.data = data
        self.color = color
        self.left = None
        self.right = None
        self.parent = None