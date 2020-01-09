#!env python
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises. 
#
# REFERENCES and CREDITS: 
#   Goodrich et al, DATA STRUCTURES AND ALGORITHMS IN PYTHON (2013), Wiley


from abstract_base.Queue import QueueBase

class Empty(Exception):
    pass

# Potential issue with using Python list is that Python will generally allocate 
# more memory than is needed in anticipation of append operations. To optimize 
# storage usage, we will cycle through empty portion of array until resize is 
# needed.

class ArrayQueue(QueueBase):
    '''ArrayQueue ADT implemented using python list as underlying storage.'''
    DEFAULT_CAPACITY = 10

    def __init__(self, build_list: list = None):
        self._front = 0 # a pointer keeping track of "front" of the queue
        self._size = 0
        if build_list:
            self._data = [None] * len(build_list)
            for elem in build_list:
                self += elem
        else:
            self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
    
    def __contains__(self, key):
        # Override Queue ABC
        '''Return True if element 'key' is contained in Queue.'''
        return (key in self._data)

    def __len__(self):
        # Override Queue ABC
        return self._size

    def __str__(self):
        if self.is_empty():
            return " >> DEBUG ArrayQueue is empty."
        return f" >> DEBUG ArrayQueue {len(self)}: {self._data}"

    def count(self, elem) -> int:
        '''Return the number of occurrences of element "elem" in the queue'''
        return self._data.count(elem)

    def dequeue(self):
        # Override Queue ABC
        '''Return front/head element from the queue.'''
        if self.is_empty():
            raise Empty("Queue is empty. Cannot dequeue.")
        if 0 < self._size < len(self._data)//4:
            # halve array capacity if virtual size is below a fourth of actual
            # capacity. Otherwise, we may have massive memory hold up.
            self._resize(len(self_data)//2)
        elem = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1)%len(self._data)  # cycle
        self._size -= 1
        return elem
        
    def enqueue(self, elem):
        # Override Queue ABC
        '''Enqueing element to the back of the queue.'''
        if self._size == len(self._data):
            # doubling capacity if virtual size reached maximum capacity
            self._resize(2*len(self._data))
        next_avail = (self._front + self._size) % len(self._data) 
        self._data[next_avail] = elem
        self._size += 1

    def first(self):
        # Override Queue ABC
        '''Return the next dequeue (head) element in the queue.
           Raise Empty exception if Queue is empty.
        '''
        if self.is_empty():
            # Can't use None becuase it may be a valid object.
            raise Empty("Queue is empty.")
        return self._data[self._front]

    def index(self, elem) -> int:
        '''Search for element 'elem' starting from front of the queue and 
           return its first index found. This index value represents the number
           of times Queue.dequeue() must be called to reach 'elem'.

           Return None if element is not found.
        '''
        try:
            array_index = self._data.index(elem)
            return self._front + len(self) - array_index + 1
        except ValueError:
            return None

    def reverse(self):
        # Override Queue ABC
        '''Reverse queue in-place'''
        if len(self) > 1:
            front_idx = self._front
            back_idx = front_idx + len(self) - 1
            for i in range(len(self)//2):
                self._data[front_idx + i], self._data[back_idx - i] \
                        = self._data[back_idx - i], self._data[front_idx + i]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Private helper methods

    def _resize(self, capacity: int):
        '''Resize array and re-index old list for amortized performance cost'''
        assert capacity >= 0
        orig_list = self._data
        walk = self._front # starting position of walk
        self._front = 0
        self._data = [None] * capacity # new capacity
        for x in range(self._size):
            self._data[x] = orig_list[walk] # shift indices and copy
            walk = (walk + 1)%len(orig_list)


class LinkedQueue(QueueBase):
    '''LinkedQueue ADT implemented using circular linked-list.'''
    class _Node:
        __slots__ = ("_elem", "_next")
        def __init__(self, elem, n=None):
            self._elem = elem
            self._next = n

        def __str__(self):
            text = f"NODE<{id(self)}> :: NEXT<{id(self._next)}> "
            text += f":: ELEM({self._elem})"
            return text
        
        def element(self):
            return self._elem
        
    def __init__(self, build_list: list = None):
        self._tail = None  # tail._next gives us head of queue.
        self._size = 0
        if build_list:
            for elem in build_list:
                self += elem

    def __contains__(self, key):
        # Override Queue ABC
        '''Return True if element 'key' is contained in Queue.'''
        walk = self._tail._next
        while walk is not self._tail:
            if key == walk.element():
                return True
            walk = walk._next
        return False

    def __len__(self):
        # Override Queue ABC
        return self._size

    def __str__(self):
        if self.is_empty():
            return " >> DEBUG LinkedQueue is empty."
        head = self._tail._next
        node_list = [None] * len(self)
        for idx in range(len(self)):
            node_list[idx] = str(head.element())
            head = head._next
        return f" >> DEBUG LinkedQueue [{len(self)}]: {', '.join(node_list)}"

    def count(self, elem) -> int:
        '''Return the number of occurrences of element "elem" in the queue'''
        walk = self._tail._next
        ans = 0
        for _ in range(self._size):
            if walk.element() == elem:
                ans += 1
            walk = walk._next
        return ans
    
    def dequeue(self):
        # Override Queue ABC
        '''Return front/head element from the queue.'''
        if self.is_empty():
            raise Empty("Queue is empty. Cannot dequeue.")
        head = self._tail._next
        if self._size == 1:
            self._tail = None
        else:
            self._tail._next = head._next
        self._size -= 1
        return head.element()

    def enqueue(self, elem):
        # Override Queue ABC
        '''Enqueing element to the back of the queue.'''
        new_node = self._Node(elem)
        if self.is_empty():
            new_node._next = new_node
        else:
            new_node._next = self._tail._next
            self._tail._next = new_node
        self._tail = new_node
        self._size += 1

    def first(self):
        # Override Queue ABC
        '''Return the next dequeue (head) element in the queue.'''
        if self.is_empty():
            # Can't use None becuase it may be a valid object.
            raise Empty("Queue is empty.")
        head = self._tail._next
        return head.element()

    def index(self, elem):
        '''Search for element 'elem' starting from front of the queue and 
           return its first index found. This index value represents the number
           of times Queue.dequeue() must be called to reach 'elem'.

           Return None if element is not found.
        '''
        walk = self._tail._next
        idx = 1
        while walk is not self._tail:
            if elem == walk.element():
                return idx
            walk = walk._next
            idx += 1
        return None 

    def reverse(self):
        # Override Queue ABC
        '''Reverse queue in-place'''
        if self.is_empty():
            raise Empty("Queue is empty.")
        if self._size > 1:
            prev = self._tail
            head = self._tail._next
            walk = self._tail._next
            self._tail = walk
            for _ in range(len(self)):
                walk = walk._next
                head._next = prev
                prev = head
                head = walk
