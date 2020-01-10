#!env python
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises. 


from abc import ABCMeta, abstractmethod

class PQBase(metaclass=ABCMeta):
    '''Abstract base class for Priority Queue.'''
    class _Item:
        __slots__ = ("_key", "_elem")
        def __init__(self, key, value):
            self._key = key
            self._elem = value

        def __ge__(self, other):
            '''Compare order of Item by priority key'''
            return self._key >= other._key

        def __gt__(self, other):
            '''Compare order of Item by priority key'''
            return self._key > other._key

        def __le__(self, other):
            '''Compare order of Item by priority key'''
            return self._key <= other._key

        def __lt__(self, other):
            '''Compare order of Item by priority key'''
            return self._key < other._key

        def __str__(self):
            return f"({self._key}, {self._elem})"

        def __repr__(self):
            return f"({self._key},{self._elem})"

        def element(self):
            return self._elem

        def priority(self):
            return self._key

    @abstractmethod
    def __contains__(self, elem):
        '''Return True if PQ contained an element "elem".'''
        ...

    @abstractmethod
    def __len__(self):
        ...

    @abstractmethod
    def __next__(self):
        ...

    @abstractmethod
    def add(self, item: _Item):
        '''Add Item into PQ'''
        ...

    @abstractmethod
    def merge(self, other):
        '''Merge the other PQ into this PQ.'''
        ...

    @abstractmethod
    def peek(self) -> _Item:
        '''Return the top-priority key-value Item from PQ.'''
        ...

    @abstractmethod
    def pop(self) -> _Item:
        '''Remove and return top-priority Item from PQ.'''
        ...

    def __add__(self, item: _Item):
        '''PQ = PQ + Item'''
        self.add(item)
        return self

    def __bool__(self):
        '''Non-empty PQ is True'''
        return len(self) > 0

    def __iadd__(self, item: _Item):
        '''PQ += Item'''
        self.add(item)
        return self

    def is_empty(self) -> bool:
        return len(self) == 0
