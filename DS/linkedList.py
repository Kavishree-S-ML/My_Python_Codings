""" LINKED LISTS """


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # Add Element at the beginning of the List
    def push(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    # Delete the Element at the specified position
    def delete(self, position):
        temp = self.head

        if position == 0:
            temp = temp.next
            self.head = temp
            return
        else:
            for i in range(position - 1):
                temp = temp.next
                if temp is None:
                    break
            if temp is None:
                print "Position beyond the node's number"
                return
            next = temp.next.next
            temp.next = None
            temp.next = next
            return

    # Get the Count of teh Linked List
    def getCount(self):
        temp = self.head
        count = 0
        while temp:
            temp = temp.next
            count += 1
        return count

    # Search for the Given Element
    def search(self, data):
        temp = self.head
        if temp is None:
            print "Linked List is Empty"
            return False
        else:
            while temp:
                if temp.data == data:
                    return True
                temp = temp.next
            return False

    # Swap two Element in the Linked List
    def swap(self, x, y):
        if x == y:
            return

        prevx = None
        currx = self.head
        while currx != None and currx.data != x:
            prevx = currx
            currx = currx.next

        prevy = None
        curry = self.head
        while curry != None and curry.data != y:
            prevy = curry
            curry = curry.next

        if currx == None and curry == None:
            return
        else:
            temp = currx
            prevx.next = curry
            prevy.next = currx
            currx.next = curry.next
            curry.next = temp

    # Get the Nth Node data
    def getNth(self, n):
        temp = self.head
        count = 0
        while temp:
            if count == n:
                return temp.data
            temp = temp.next
            count += 1
        return 0

    # Reverse the Element in the Linked List
    def reverse(self):
        temp = self.head
        prev = None
        while temp:
            next = temp.next
            temp.next = prev
            prev = temp
            temp = next
        self.head = prev

    # Delete the Linked List
    def deleteList(self):
        temp = self.head
        while temp:
            prev = temp.next
            del temp.data
            temp = prev

    # Print the Linked List
    def printList(self):
        temp = self.head
        while temp:
            print temp.data,
            temp = temp.next


llist = LinkedList()
for i in range(0, 6):
    llist.push(i)
print "Linked List --> ",
llist.printList()
print "\nCount of the Linked List : %d " %(llist.getCount())
if llist.search(11):
    print "Element Found"
else:
    print "Element doesn't exist"
xFound = llist.getNth(1)
if xFound != 0:
    print "Element at the specified index is  : %d" %xFound
else:
    print "Nth element is None"
llist.swap(4,3)
print "Linked List(After deleting element at position 'x') --> ",
llist.delete(5)
llist.printList()
llist.reverse()
print "\nLinked List after reversed --> ",
llist.printList()
"""
llist.deleteList()
print "\nDeleting Linked List Completely : ",
llist.printList()
"""
