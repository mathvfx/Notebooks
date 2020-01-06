#!env python
from abc import ABCMeta, abstractmethod

class Queue(metaclass=ABCMeta):
    @abstractmethod
    def __len__(self):
        ...

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

    def __iadd__(self, elem):
        self.enqueue(elem)
        return self

    def is_empty(self):
        return len(self) == 0
