#!env python
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises. 
#

from abc import ABCMeta, abstractmethod

class DEQue(metaclass=ABCMeta):
    '''Double-Ended Queue implementations. 
       For production, use collections.deque instead.
    '''
    @abstractmethod
    def __len__(self):
        ...

    @abstractmethod
    def __contains__(self, elem):
        '''Return True if Deque contains "elem"'''

    @abstractmethod
    def back(self):
        '''Return last element of the queue.'''

    @abstractmethod
    def dequeue(self):
        '''Remove and return last element of the queue.'''

    @abstractmethod
    def dequeue_back(self):
        '''Remove and return first element of the queue.'''

    @abstractmethod
    def enqueue(self, elem):
        '''Add elem to the back of the queue. 
           Meaning of "back" is equivalent to index n of n-sized array.
        '''

    @abstractmethod
    def enqueue_back(self, elem):
        '''Add elem to the front of the queue. 
           Meaning of "front" is equivalent to index 0 of n-sized array.
        '''

    @abstractmethod
    def front(self):
        '''Return first element of the queue.'''

    @abstractmethod
    def reverse(self):
        '''Reverse queue'''

    def is_empty(self):
        return len(self) == 0
