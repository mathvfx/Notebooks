#!env python
from abc import ABCMeta, abstractmethod

class DEQue(metaclass=ABCMeta):
    '''Double-Ended Queue implementations. 
       For production, use collections.deque instead.
    '''
    @abstractmethod
    def __len__(self):
        ...

    @abstractmethod
    def append_back(self, elem):
        '''Add elem to the back of the queue. 
           Meaning of "back" is equivalent to index n of n-sized array.
        '''

    @abstractmethod
    def append_front(self, elem):
        '''Add elem to the front of the queue. 
           Meaning of "front" is equivalent to index 0 of n-sized array.
        '''

    @abstractmethod
    def pop_back(self):
        '''Remove and return last element of the queue.'''

    @abstractmethod
    def pop_front(self):
        '''Remove and return first element of the queue.'''

    @abstractmethod
    def first(self):
        '''Return first element of the queue.'''

    @abstractmethod
    def last(self):
        '''Return last element of the queue.'''

    def is_empty(self):
        return len(self) == 0
