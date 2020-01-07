#!env python
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises. 
#

from abc import ABCMeta, abstractmethod

class Queue(metaclass=ABCMeta):
    @abstractmethod
    def __len__(self):
        ...

    @abstractmethod
    def __contains__(self, elem):
        '''Return True if Queue contains "elem"'''

    @abstractmethod
    def dequeue(self):
        '''Remove and return first (or bottom or beginning) element of the 
           queue
        '''

    @abstractmethod
    def enqueue(self, elem):
        '''Add elem to the back (or top or end) of the queue'''

    @abstractmethod
    def first(self):
        '''Return first (bottom or beginning) element of the queue'''

    @abstractmethod
    def reverse(self):
        '''Reverse queue'''

    def __iadd__(self, elem):
        self.enqueue(elem)
        return self

    def is_empty(self):
        return len(self) == 0
