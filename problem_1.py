class LinkedListNode:
    
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.pre = None
        
class LRU_Cache(object):

    def __init__(self, capacity):
        # Initialize class variables
        self.capacity = capacity
        self.table = [None]*capacity
        self.num = 0
        self.head = None
        self.tail = None
        self.dict = dict() # store [key: node key, value: node]
        pass
    
    def update_dict(self, node):
        self.dict[node.key] = node
    
    def delete_node(self, node):
        self.dict[node.key] = None

    def find_node(self, key):
        if key not in self.dict: 
            return None
        return self.dict[key]           

    def get(self, key):
        # Retrieve item from provided key. Return -1 if nonexistent. 
        # current = self.head
        # while current != None and current.key != key:
        #     current = current.next
        if self.find_node(key) == None:
            return -1
        current = self.find_node(key)
        if current != self.head:
            current.pre.next = current.next
            self.update_dict(current.pre)
            if current.next != None:
                current.next.pre = current.pre
                self.update_dict(current.next)
            if self.tail == current:
                self.tail = current.pre
            current.next = self.head
            current.next.pre = current
            self.update_dict(current.next)
            current.pre = None
            self.head = current
            self.update_dict(current)
        return current.value
        pass

    def set(self, key, value):
        # Set the value if the key is not present in the cache. If the cache is at capacity remove the oldest item. 
        self.num += 1
        if key in self.dict:
            return
        new_node = LinkedListNode(key, value)
        if self.num > self.capacity:
            if self.tail.pre != None:
                self.tail = self.tail.pre
                self.delete_node(self.tail.next)
                self.tail.next = None
                self.update_dict(self.tail)
#                 print("tail key: ", self.tail.key, " value: ", self.tail.value)
            else:
                self.tail = new_node
            self.num -= 1
        if self.head == None:
            self.head = new_node
            self.tail = new_node
        else:
            if self.tail == new_node:
                self.head == new_node
            else:
                new_node.next = self.head
                self.head.pre = new_node
                if self.tail.pre == None and self.num > 1:
                    self.head.next = self.tail
                    self.tail.pre = self.head
                self.update_dict(self.head)
                self.update_dict(self.tail)
                self.head = new_node
#                 print("head key: ", self.head.key, " value: ", self.head.value)
        self.update_dict(new_node)

        pass
    
    def print(self):
        current = self.head
        num = 0
        while current != None:
            print("num: ", num, " key: ", current.key, " value: ", current.value)
            current = current.next
            num += 1
        print("\n")
        
# Test Cases

# our_cache = LRU_Cache(5)

# our_cache.set(1, 1)
# our_cache.set(2, 2)
# our_cache.set(3, 3)
# our_cache.set(4, 4)

# print(our_cache.get(1))       # returns 1
# our_cache.print()

# print(our_cache.get(2))       # returns 2
# our_cache.print()

# print(our_cache.get(9))      # returns -1 because 9 is not present in the cache
# our_cache.print()

# our_cache.set(5, 5) 
# our_cache.print()

# our_cache.set(6, 6)
# our_cache.print()

# print(our_cache.get(3))      # returns -1 because the cache reached it's capacity and 3 was the least recently used entry
# our_cache.print()
