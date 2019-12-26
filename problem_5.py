import hashlib
import datetime

class Block:

    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calc_hash()
        
    def calc_hash(self):
        sha = hashlib.sha256()

        # hash_str = self.data.encode('utf-8')
        hash_str = f'{self.timestamp}\n{self.data}\n{self.previous_hash}'.encode('utf-8')

        sha.update(hash_str)

        return sha.hexdigest()
    
    def __repr__(self):
        s = "Block details: \n"
        s += "Data         : " + self.data + "\n"
        s += "Previous hash: " + self.previous_hash + "\n"
        s += "Hash         : " + self.hash + "\n"
        return s

class LinkedListNode:
    
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        
class HashMap: # key:hash, value:block node

    def __init__(self, initial_size = 10):
        self.bucket_array = [None for _ in range(initial_size)]
        self.p = 31
        self.num_entries = 0

    def put(self, key, value):
        bucket_index = self.get_bucket_index(key)

        new_node = LinkedListNode(key, value)
        head = self.bucket_array[bucket_index]

        # check if key is already present in the map, and update it's value
        while head is not None:
            if head.key == key:
                head.value = value
                return
            head = head.next

        # key not found in the chain --> create a new entry and place it at the head of the chain
        head = self.bucket_array[bucket_index]
        new_node.next = head
        self.bucket_array[bucket_index] = new_node
        self.num_entries += 1
        
    def get(self, key):
        if key == 0:
            return None
        bucket_index = self.get_hash_code(key)
        head = self.bucket_array[bucket_index]
        while head is not None:
            if head.key == key:
                return head.value
            head = head.next
        return None
        
    def get_bucket_index(self, key):
        bucket_index = self.get_hash_code(key)
        return bucket_index
    
    def get_hash_code(self, key):
        key = str(key)
        num_buckets = len(self.bucket_array)
        current_coefficient = 1
        hash_code = 0
        for character in key:
            hash_code += ord(character) * current_coefficient
            hash_code = hash_code % num_buckets                       # compress hash_code
            current_coefficient *= self.p
            current_coefficient = current_coefficient % num_buckets   # compress coefficient

        return hash_code % num_buckets                                # one last compression before returning
    
    def size(self):
        return self.num_entries
        
class BlockChain:
    def __init__(self):
        self.head = None
        self.tail = None
        self.hashmap = HashMap()
        
    def prepend(self, data):
        """ Prepend a value to the beginning of the list. """
        
        if self.head == None:
            self.head = Block(datetime.datetime.now(), data, 0)
            self.hashmap.put(self.head.hash, self.head)
            return
        new_node = Block(datetime.datetime.now(), data, self.head.hash)
        self.head = new_node
        self.hashmap.put(new_node.hash, new_node)
        pass
    
    def append(self, data):
        """ Append a value to the end of the list. """
        
        if self.head == None:
            self.head = Block(datetime.datetime.now(), data, 0)
            self.hashmap.put(self.head.hash, self.head)
            print("blockchain empty, adding head")
            return
        current_node = self.head
        i = 0
        while current_node.previous_hash != 0:
#             print("append i: ", i)
#             print("c_node data: ", current_node.data)
            current_node = self.hashmap.get(current_node.previous_hash)
            i += 1
#         print("current data: ", current_node.data)
        new_node = Block(datetime.datetime.now(), data, 0)
        current_node.previous_hash = new_node.hash
        self.hashmap.put(current_node.hash, current_node)
        self.hashmap.put(new_node.hash, new_node)
        pass
    
    def search(self, data):
        """ Search the linked list for a node with the requested value and return the node. """
        
        if self.head == None:
            return None
        current_node = self.head
        while current_node.data != data:
            current_node = self.hashmap.get(current_node.previous_hash)
        if current_node != None:
            print("Block found.")
            return current_node
        else:
            raise ValueError("Block not found in the list.")
        pass
    
    def remove(self, data):
        """ Remove first occurrence of value. """
        
        if self.head == None:
            return
        if self.hashmap.get(self.head.hash).data == data:
            self.hashmap.put(self.head.hash, None)
            self.head = self.hashmap.get(self.head.previous_hash)
            return
        current_node = self.head
        next_node = self.hashmap.get(current_node.previous_hash)
        while next_node != None:
            if next_node.data == data:
                next_next_node = self.hashmap.get(next_node.previous_hash)
                if next_next_node != None:
                    current_node.previous_hash = next_next_node.hash
                else:
                    current_node.previous_hash = 0
                self.hashmap.put(next_node.hash, None)
                self.hashmap.put(current_node.hash, current_node)
                return
            current_node = next_node
            next_node = self.hashmap.get(current_node.previous_hash)
        if next_node == None:
            raise ValueError("Value not found in the list.")
        pass
    
    def pop(self):
        """ Return the first node's value and remove it from the list. """
        
        if self.head == None:
            return None
        first_node = self.head
        self.head = self.hashmap.get(first_node.previous_hash)
        self.hashmap.put(first_node.hash, None)
        return first_node.data
        pass
    
    def insert(self, data, pos):
        """ Insert value at pos position in the list. If pos is larger than the
            length of the list, append to the end of the list. """
        
        if pos <= 0:
            print("prepend as insert")
            self.prepend(data)
            return
        if pos > self.size() - 1:
            print("append as insert")
            self.append(data)
            return
        i = 0
        current_node = self.head
        next_node = self.hashmap.get(current_node.previous_hash)
        while i < pos - 1:
            current_node = next_node
            next_node = self.hashmap.get(next_node.previous_hash)
            i += 1
        new_node = Block(datetime.datetime.now(), data, 0)
        new_node.previous_hash = next_node.hash
        current_node.previous_hash = new_node.hash
        self.hashmap.put(new_node.hash, new_node)
        self.hashmap.put(current_node.hash, current_node)
        self.hashmap.put(next_node.hash, next_node)
        pass
    
    def size(self):
        """ Return the size or length of the linked list. """
        
        current_node = self.head
        i = 0
        while current_node != None:
#             print("c_node data: ", current_node.data)
            current_node = self.hashmap.get(current_node.previous_hash)
            i += 1
        return i
        pass
    
    def __repr__(self):
        if self.size() > 0:
            s = "<start here>\n_________________\n" 
            current_node = self.head 
            while current_node != None:
                s += "\n_________________".join([current_node.data,"\n"])
                current_node = self.hashmap.get(current_node.previous_hash)
            s += "<end here>\n"
            return s
        else:
            return "<blockchain is empty>\n"


# Test Cases

blockchain = BlockChain()
data = "abcde"
blockchain.append(data)
# print("blockchain size: ", blockchain.size())
# print("hashmap size: ", blockchain.hashmap.size())
# print("\n")

data = "bcdef"
blockchain.append(data)
# print("blockchain size: ", blockchain.size())
# print("hashmap size: ", blockchain.hashmap.size())
# print("\n")

data = "cdefg"
blockchain.append(data)
# print("blockchain size: ", blockchain.size())
# print("hashmap size: ", blockchain.hashmap.size())
# print("\n")

data = "defgh"
blockchain.append(data)
# print("blockchain size: ", blockchain.size())
# print("hashmap size: ", blockchain.hashmap.size())
# print("\n")

data = "efghi"
blockchain.prepend(data)
# print("blockchain size: ", blockchain.size())
# print("hashmap size: ", blockchain.hashmap.size())
# print("\n")

print("searching data")
block0 = blockchain.search(data)
# print(block0)
# print(blockchain)

print("removing head")
blockchain.remove(data) # remove head
# print(blockchain)
# print("blockchain size: ", blockchain.size())
# print("\n")

print("removing middle data")
data = "bcdef"
blockchain.remove(data) # remove mid data
# print(blockchain)
# print("blockchain size: ", blockchain.size())
# print("\n")

print("removing tail")
data = "defgh"
blockchain.remove(data) # remove tail
# print(blockchain)
# print("blockchain size: ", blockchain.size())
# print("\n")

print("popping front")
data = blockchain.pop()
# print("pop data: ", data)
# print(blockchain)
# print("blockchain size: ", blockchain.size())
# print("\n")

print("popping front")
data = blockchain.pop()
# print("pop data: ", data)
# print(blockchain)
# print("blockchain size: ", blockchain.size())
# print("\n")

print("addding blocks back")
data = "abcde"
blockchain.append(data)
data = "bcdef"
blockchain.append(data)
data = "cdefg"
blockchain.append(data)
data = "defgh"
blockchain.append(data)
data = "efghi"
blockchain.prepend(data)
# print("blockchain size: ", blockchain.size())
# print("hashmap size: ", blockchain.hashmap.size())
# print("\n")

print("inserting")
data = "fghij"
blockchain.insert(data, 0) # insert head
# print(blockchain)
# print("blockchain size: ", blockchain.size())
# print("\n")

print("inserting")
data = "ghijk"
blockchain.insert(data, blockchain.size()) # insert tail
# print(blockchain)
# print("blockchain size: ", blockchain.size())
# print("\n")

print("inserting")
data = "hijkl"
blockchain.insert(data, 3) # insert middle
# print(blockchain)
# print("blockchain size: ", blockchain.size())
# print("\n")
