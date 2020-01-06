#!env python
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises to 
# become better software developer. It may not be robust enough for production.
#

from abc import ABCMeta, abstractmethod

class Stack(metaclass=ABCMeta):
    '''Implement ADT using last-in, first-out (LIFO) principle.'''
    @abstractmethod
    def __len__(self):
        ...

    @abstractmethod
    def push(self, elem):
        '''Add elem to the top of the stack'''

    @abstractmethod
    def pop(self):
        '''Remove and return top element in the stack'''

    @abstractmethod
    def top(self):
        '''Return top element in the stack'''

    def __iadd__(self, elem):
        self.push(elem)
        return self

    def is_empty(self):
        return len(self) == 0
