class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return str(self.value)


class LinkedList:
    def __init__(self):
        self.head = None

    def __str__(self):
        cur_head = self.head
        out_string = ""
        while cur_head:
            out_string += str(cur_head.value) + " -> "
            cur_head = cur_head.next
        return out_string


    def append(self, value):

        if self.head is None:
            self.head = Node(value)
            return

        node = self.head
        while node.next != None:
            node = node.next

        node.next = Node(value)

    def size(self):
        size = 0
        node = self.head
        while node:
            size += 1
            node = node.next

        return size

def union(llist_1, llist_2):
    # Your Solution Here
    output = LinkedList()
    dict1 = dict()
    c_node1 = llist_1.head
    c_node2 = llist_2.head
    while c_node1 != None or c_node2 != None:
        if c_node1 != None:
            if c_node1.value not in dict1:
                dict1[c_node1.value] = 1
                output.append(c_node1.value)
            c_node1 = c_node1.next
        if c_node2 != None:
            if c_node2.value not in dict1:
                dict1[c_node2.value] = 1
                output.append(c_node2.value)
            c_node2 = c_node2.next 
    return output
    pass

def intersection(llist_1, llist_2):
    # Your Solution Here
    output = LinkedList()
    dict1 = dict()
    c_node = llist_1.head
    while c_node != None:
        if c_node.value not in dict1:
            dict1[c_node.value] = 1
        c_node = c_node.next
    dict2 = dict()
    c_node = llist_2.head
    while c_node != None:
        if c_node.value in dict1 and c_node.value not in dict2:
            output.append(c_node.value)
            dict2[c_node.value] = 1
        c_node = c_node.next
    return output
    pass


# Test case 1

linked_list_1 = LinkedList()
linked_list_2 = LinkedList()

element_1 = [3,2,4,35,6,65,6,4,3,21]
element_2 = [6,32,4,9,6,1,11,21,1]

for i in element_1:
    linked_list_1.append(i)

for i in element_2:
    linked_list_2.append(i)

# print (union(linked_list_1,linked_list_2))
# print (intersection(linked_list_1,linked_list_2))

# Test case 2

linked_list_3 = LinkedList()
linked_list_4 = LinkedList()

element_1 = [3,2,4,35,6,65,6,4,3,23]
element_2 = [1,7,8,9,11,21,1]

for i in element_1:
    linked_list_3.append(i)

for i in element_2:
    linked_list_4.append(i)

# print (union(linked_list_3,linked_list_4))
# print (intersection(linked_list_3,linked_list_4))

# Test case 3

linked_list_5 = LinkedList()
linked_list_6 = LinkedList()

element_1 = [1,2,4,12,3,4,7,11,5,8,1]
element_2 = [1,7,8,9,11,21,1]

for i in element_1:
    linked_list_5.append(i)

for i in element_2:
    linked_list_6.append(i)

# print (union(linked_list_5,linked_list_6))
# print (intersection(linked_list_5,linked_list_6))

# Test case 4

linked_list_7 = LinkedList()
linked_list_8 = LinkedList()

element_1 = []
element_2 = [1,7,8,9,11,21,1]

for i in element_1:
    linked_list_7.append(i)

for i in element_2:
    linked_list_8.append(i)

# print (union(linked_list_7,linked_list_8))
# print (intersection(linked_list_7,linked_list_8))

# Test case 4

linked_list_9 = LinkedList()
linked_list_10 = LinkedList()

element_1 = []
element_2 = []

for i in element_1:
    linked_list_9.append(i)

for i in element_2:
    linked_list_10.append(i)

# print (union(linked_list_9,linked_list_10))
# print (intersection(linked_list_9,linked_list_10))

