#!env python

# REFERENCES and CREDITS: 
#   Goodrich et al, DATA STRUCTURES AND ALGORITHMS IN PYTHON (2013), Wiley

from abstract_base.Queue import Queue

class Empty(Exception):
    pass

class ArrayQueue(Queue):
    '''ArrayQueue ADT. Implemented using python list as underlying storage.

       Potential issue with using Python list is that Python will generally 
       allocate more memory than is needed in anticipation of append operations.
       To optimize storage usage, we will cycle through empty portion of array
       until resize is needed.
    '''
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

    def __len__(self):
        # Override Queue ABC
        return self._size

    def __str__(self):
        if self.is_empty():
            return " >> DEBUG ArrayQueue is empty."
        return f" >> DEBUG ArrayQueue {len(self)}: {self._data}"

    def dequeue(self):
        # Override Queue ABC
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
        if self._size == len(self._data):
            # doubling capacity if virtual size reached maximum capacity
            self._resize(2*len(self._data))
        next_avail = (self._front + self._size) % len(self._data) 
        self._data[next_avail] = elem
        self._size += 1

    def first(self):
        # Override Queue ABC
        if self.is_empty():
            return None
        return self._data[self._front]

    def reverse(self):
        '''Reverse queue (in-place)'''
        if len(self) > 1:
            front_idx = self._front
            back_idx = front_idx + len(self) - 1
            for i in range(len(self)//2):
                self._data[front_idx + i], self._data[back_idx - i] \
                        = self._data[back_idx - i], self._data[front_idx + i]

    def _resize(self, capacity: int):
        '''Resize array and re-index old content'''
        assert capacity >= 0
        orig_list = self._data
        walk = self._front # starting position of walk
        self._front = 0
        self._data = [None] * capacity # new capacity
        for x in range(self._size):
            self._data[x] = orig_list[walk] # shift indices and copy
            walk = (walk + 1)%len(orig_list)


class LinkedQueue(Queue):
    '''LinkedQueue ADT. Implemented using circular linked-list.

       Keeping in mind that every linked node require a little more storage 
       space than an array.
    '''
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
    
    def dequeue(self):
        # Override Queue ABC
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
        if self.is_empty():
            return None
        head = self._tail._next
        return head.element()

    def reverse(self):
        '''Reverse queue (in-place'''
        if self.is_empty():
            raise Empty("Queue is empty")
        if self._size > 1:
            prev = self._tail
            head = self._tail._next
            walk = self._tail._next
            self._tail = walk
            for i in range(len(self)):
                walk = walk._next
                head._next = prev
                prev = head
                head = walk
