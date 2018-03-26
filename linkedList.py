""" LINKED LISTS """


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def printList(self):
        temp = self.head
        while temp:
            print temp.data,
            temp = temp.next


llist = LinkedList()
for i in range(0, 5):
    llist.push(i)
llist.printList()
