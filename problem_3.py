from collections import deque
from operator import itemgetter, attrgetter
import sys

class Node(object):
        
    def __init__(self,value = None):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        
    def set_value(self,value):
        self.value = value
        
    def get_value(self):
        return self.value
        
    def set_parent(self, parent):
        self.parent = parent
        
    def set_left_child(self,left):
        self.left = left
        if left != None:
            left.set_parent(self)
        
    def set_right_child(self, right):
        self.right = right
        if right != None:
            right.set_parent(self)
    
    def get_parent(self):
        return self.parent
        
    def get_left_child(self):
        return self.left
    
    def get_right_child(self):
        return self.right

    def has_left_child(self):
        return self.left != None
    
    def has_right_child(self):
        return self.right != None
    
    def has_parent(self):
        return self.parent != None
    
    # define __repr_ to decide what a print statement displays for a Node object
    def __repr__(self):
        return f"Node({self.get_value()})"
    
    def __str__(self):
        return f"Node({self.get_value()})"

class PriorityQueue():
    def __init__(self):
        self.q = list()
        
    def enq(self,value):
        self.q.append(value)
#         self.q.sort(key=itemgetter(2),reverse=True)
        
    def deq(self):
        if len(self.q) > 0:
            self.q.sort(key=itemgetter(2),reverse=True)
            return self.q.pop()
        else:
            return None
    
    def __len__(self):
        return len(self.q)
    
    def __repr__(self):
        if len(self.q) > 0:
            s = "<enqueue here>\n_________________\n" 
            s += "\n_________________\n".join([str(item) for item in self.q])
            s += "\n_________________\n<dequeue here>"
            return s
        else:
            return "<queue is empty>"
        
class Queue():
    def __init__(self):
        self.q = list()
        
    def enq(self,value):
        self.q.append(value)
        
    def deq(self):
        if len(self.q) > 0:
            return self.q.pop()
        else:
            return None
    
    def __len__(self):
        return len(self.q)
    
    def __repr__(self):
        if len(self.q) > 0:
            s = "<enqueue here>\n_________________\n" 
            s += "\n_________________\n".join([str(item) for item in self.q])
            s += "\n_________________\n<dequeue here>"
            return s
        else:
            return "<queue is empty>"


class Tree():
    def __init__(self):
        self.root = None
        
    def set_root(self,value):
        self.root = Node(value)
        
    def get_root(self):
        return self.root
            
    def __repr__(self):
        level = 0
        q = Queue()
        visit_order = list()
        node = self.get_root()
        q.enq( (node,level) )
        while(len(q) > 0):
            node, level = q.deq()
            if node == None:
                visit_order.append( ("<empty>", level))
                continue
            visit_order.append( (node, level) )
            if node.has_left_child():
                q.enq( (node.get_left_child(), level +1 ))
            else:
                q.enq( (None, level +1) )

            if node.has_right_child():
                q.enq( (node.get_right_child(), level +1 ))
            else:
                q.enq( (None, level +1) )

        s = "Tree\n"
        previous_level = -1
        for i in range(len(visit_order)):
            node, level = visit_order[i]
            if level == previous_level:
                s += " | " + str(node) 
            else:
                s += "\n" + str(node)
                previous_level = level

                
        return s

def path_from_root_to_node(root, char):
    output = path_from_node_to_root(root, char)
    return list(reversed(output))

def path_from_node_to_root(root, char):
#     print(root)
    if root is None:
        return None

    elif root.get_value()[0] == char:
        return []

    left_answer = path_from_node_to_root(root.left, char)
    if left_answer is not None:
        left_answer.append(0)
        return left_answer

    right_answer = path_from_node_to_root(root.right, char)
    if right_answer is not None:
        right_answer.append(1)
        return right_answer
    return None


# Note: priority queue pq has element [Node, char, num]
def huffman_encoding(data):
    tree = Tree()
    char_dict = dict()
    for i in range(len(data)):
        if data[i] not in char_dict:
            char_dict[data[i]] = 1
        else:
            char_dict[data[i]] += 1
    # print("char_dict: ", char_dict)
    pq = PriorityQueue()
    for (k,v) in char_dict.items():
        pq.enq([None,k,v])
    # print(pq)
    # print("char_num: ", len(char_dict))
    char_num = len(char_dict)
    node_dict = dict()
    for i in range(1, char_num):
        new_node = Node()
        left = pq.deq()
        if left[0] is None:
            left_node = Node(left[1:3])
        else:
            left_node = left[0]
        new_node.set_left_child(left_node)
        right = pq.deq()
        if right[0] is None:
            right_node = Node(right[1:3])
        else:
            right_node = right[0]
        new_node.set_right_child(right_node)
        new_node.set_value([None, left_node.get_value()[1] + right_node.get_value()[1]])
        pq.enq([new_node] + new_node.get_value())
        # print("pq: ", pq)
#         print("left_node: ", left_node, "right_node: ", right_node)
    tree_root_temp = pq.deq()
    if tree_root_temp != None:
        tree.root = tree_root_temp[0]
        if tree.root == None:
            tree.root = Node([None, None])
            new_node = Node(tree_root_temp[1:3])
            tree.root.set_left_child(new_node)
    else:
        tree.root = None
        print("root is empty")
        return "0", tree
    # print(tree)
#     print(tree.root.get_left_child())
#     print(tree.root.get_right_child())
#     print(tree.root.get_value()[0])
    output = []
    for i in range(len(data)):
        code = path_from_root_to_node(tree.root, data[i])
        output += code 
    output_str = ""
    for i in range(len(output)):
        output_str += str(output[i])
    # print("output: ", output_str)
    return output_str, tree
    pass

def huffman_decoding(data,tree):
    i = 0
    node = tree.get_root()
    if node == None:
        return ""
    output_str = ""
    while 1:
        char = node.get_value()[0]
        if char != None:
            output_str += char
            node = tree.get_root()
            if i == len(data):
#                 print("breaking, last char:", char)
                break
        num = int(data[i])
        if num == 0:
            node = node.get_left_child()
        else:
            node = node.get_right_child()
        i += 1
#         print("output_str: ", output_str, "num: ", num)
    return output_str
    pass

if __name__ == "__main__":
    codes = {}

    # Test Case 1

    a_great_sentence = "The bird is the word"

    print ("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence)))
    print ("The content of the data is: {}\n".format(a_great_sentence))

    encoded_data, tree = huffman_encoding(a_great_sentence)

    print ("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print ("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    print ("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print ("The content of the encoded data is: {}\n".format(decoded_data))

    # Test Case 2
    print("-------------------------------------")

    a_great_sentence1 = ""

    print ("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence1)))
    print ("The content of the data is: {}\n".format(a_great_sentence1))

    encoded_data, tree = huffman_encoding(a_great_sentence1)

    print ("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print ("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    print ("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print ("The content of the encoded data is: {}\n".format(decoded_data))

    # Test Case 3
    print("-------------------------------------")

    a_great_sentence2 = "AAAAAAAAA"

    print ("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence2)))
    print ("The content of the data is: {}\n".format(a_great_sentence2))

    encoded_data, tree = huffman_encoding(a_great_sentence2)

    print ("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print ("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    print ("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print ("The content of the encoded data is: {}\n".format(decoded_data))


