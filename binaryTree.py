"""
    BINARY TREE OPERATIONS

    OPERATIONS: Insertion, Search
"""


class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.value = data


def insert(root, node):
    if root is None:
        root = node
    else:
        if root.value < node.value:
            if root.right is None:
                root.right = node
            else:
                insert(root.right, node)
        else:
            if root.left is None:
                root.left = node
            else:
                insert(root.left, node)


def inorder(root):
    if root:
        inorder(root.left)
        print root.value,
        inorder(root.right)

def inOrderFunc(root):
    temp = root
    s = []
    done = 0

    while not done:
        if temp is not None:
            s.append(temp)
            temp = temp.left
        else:
            if len(s) > 0:
                temp = s.pop()
                print temp.value,
                temp = temp.right
            else:
                done = 1

root = Node(5)
insert(root, Node(3))
insert(root, Node(7))
insert(root, Node(4))
insert(root, Node(2))
insert(root, Node(6))
inorder(root)
print "\n"
inOrderFunc(root)
