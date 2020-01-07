#!env python
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises in 
# effort to become a better software developer. 
#
# REFERENCES and CREDITS: 
#   Goodrich et al, DATA STRUCTURES AND ALGORITHMS IN PYTHON (2013), Wiley


from abstract_base.Stack import Stack


class Empty(Exception):
    pass


class ArrayStack(Stack):
    '''ArrayStack ADT implemented using python list as underlying storage.'''
    def __init__(self, build_list: list = None):
        if build_list:
            self._data = [None] * len(build_list)
            for idx, elem in enumerate(build_list):
                self._data[idx] = elem
        else:
            self._data = list()

    def __contains__(self, key):
        # Override Stack ABC
        '''Return True if element 'key' is contained in Stack.'''
        return (key in self._data)

    def __len__(self):
        # Override Stack ABC
        return len(self._data)

    def __str__(self):
        return f" >> DEBUG ArrayStack [{len(self)}]: {self._data}*"

    def index(self, elem) -> int:
        '''Search for element 'elem' starting from top of the stack and 
           return its first index found. This index value represents the number
           of times Stack.pop() must be called to reach 'elem'.

           Return None if element is not found.
        '''
        try:
            array_index = self._data.index(elem)
            return len(self) - array_index
        except ValueError:
            return None

    def pop(self):
        # Override Stack ABC
        '''Remove and return element from the top of the stack.
           Raise Empty error if empty.
        '''
        if self.is_empty():
            raise Empty("Stack is empty")
        return self._data.pop()   # using list's pop method

    def push(self, elem):
        # Override Stack ABC
        '''Push element to the top of the stack'''
        self._data.append(elem)

    def reverse(self):
        # Override Stack ABC
        '''Reverse stack in-place'''
        self._data.reverse()

    def top(self):
        # Override Stack ABC
        '''Return the next element to be popped from stack'''
        if self.is_empty():
            return None
        return self._data[-1]


class LinkedStack(Stack):
    '''LinkedStack ADT implemented using singly linked-list.'''
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
        self._head = None   # pointer to head of linked-list
        self._size = 0
        if build_list:
            for elem in build_list:
                self += elem

    def __contains__(self, key):
        # Override Stack ABC
        '''Return True if element 'key' is contained in Stack.'''
        walk = self._head
        while walk:
            if key == walk.element():
                return True
            walk = walk._next
        return False

    def __len__(self):
        # Override Stack ABC
        return self._size
    
    def __str__(self):
        if self.is_empty():
            return " >> DEBUG LinkedStack is empty."
        walk = self._head 
        node_list = [None] * len(self)
        idx = 0
        while walk:
            node_list[idx] = str(walk._elem)
            idx += 1
            walk = walk._next
        return f" >> DEBUG LinkedStack [{self._size}]: *{', '.join(node_list)}"

    def index(self, elem):
        '''Search for element 'elem' starting from top of the stack and 
           return its first index found. This index value represents the number
           of times Stack.pop() must be called to reach 'elem'.

           Return None if element is not found.
        '''
        walk = self._head
        idx = 1
        while walk:
            if elem == walk.element():
                return idx
            walk = walk._next
            idx += 1
        return None 

    def pop(self):
        # Override Stack ABC
        '''Remove and return element from the top of the stack.
           Raise Empty error if empty.
        '''
        if self.is_empty():
            raise Empty("Stack is empty. Cannot pop.")
        elem = self._head._elem
        self._head = self._head._next   # deprecate popped node
        self._size -= 1
        return elem

    def push(self, elem):
        # Override Stack ABC
        '''Push element to the top of the stack'''
        self._head = self._Node(elem, self._head)
        self._size += 1

    def reverse(self):
        # Override Stack ABC
        '''Reverse stack in-place'''
        if self.is_empty():
            raise Empty("Stack is empty.")
        if self._size > 1:
            prev = self._head   # initial state
            self._head = self._head._next  # initial state
            walk = self._head   # initial state
            prev._next = None
            while self._head._next:   # begin walk and operations
                self._head = self._head._next
                walk._next = prev
                prev = walk
                walk = self._head
            self._head._next = prev

    def top(self):
        # Override Stack ABC
        '''Return the next element to be popped from stack'''
        if self.is_empty():
            return None
        return self._head._elem
