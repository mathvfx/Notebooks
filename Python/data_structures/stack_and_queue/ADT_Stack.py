#!env python

# REFERENCES and CREDITS: 
#   Goodrich et al, DATA STRUCTURES AND ALGORITHMS IN PYTHON (2013), Wiley

from abstract_base.Stack import Stack

class Empty(Exception):
    pass

class ArrayStack(Stack):
    '''ArrayStack ADT. Implemented using python list as underlying storage.
       
       Potential issue with using Python list is that Python will generally 
       allocate more memory than is needed in anticipation of append operations.
       However, for simple array-based Stack, we simply utilize Python's List's
       built-in efficient methods.
    '''
    def __init__(self):
        self._data = list()

    def __len__(self):
        # Override Stack ABC
        return len(self._data)

    def __str__(self):
        return f" >> DEBUG ArrayStack [{len(self)}]: {self._data}"

    def pop(self):
        # Override Stack ABC
        if self.is_empty():
            raise Empty("Stack is empty")
        return self._data.pop()

    def push(self, elem):
        # Override Stack ABC
        self._data.append(elem)

    def top(self):
        # Override Stack ABC
        if self.is_empty():
            return None
        return self._data[-1]
