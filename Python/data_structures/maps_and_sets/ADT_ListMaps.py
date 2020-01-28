#!env python3
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises. 
#
# REFERENCES and CREDITS: 
#   Goodrich et al, DATA STRUCTURES AND ALGORITHMS IN PYTHON (2013), Wiley
#
#
# List Maps here does not use hashing functions to determine list indices.
# Instead, we simply use a list to store Key-Value Item into each list
# components. Sorted List Maps use Binary Search method to determine insertion 
# point for each Key-Value Items, and thereby creating a sorted list of Items. 


import bisect
from abstract_base.Maps import MapBase


class SortedMap(MapBase):
    '''Basic, concrete implementation of Maps ADT sorted by keys.'''
    def __init__(self):
        self._data = list()

    def __getitem__(self, key):
        # Override MapBase (MutableMapping) ABC
        '''Get item by 'key'. Raise KeyError if 'key' is not exist.'''
        idx = bisect.bisect_left(self._data, self._Item(key, None))
        if idx != len(self) and self._data[idx]._key == key:
            return self._data[idx]._value
        raise KeyError(f"{repr(key)} not found.")

    def __setitem__(self, key, value):
        # Override MapBase (MutableMapping) ABC
        '''Set key-value pairs.
        Value associated with 'key' will be updated if item already exists.
        '''
        idx = bisect.bisect_left(self._data, self._Item(key, None))
        if idx < len(self) and self._data[idx]._key == key:
            self._data[idx]._value = value
        else:
            self._data.insert(idx, self._Item(key, value))

    def __delitem__(self, key):
        # Override MapBase (MutableMapping) ABC
        '''Delete Item by 'key'. Raise KeyError if 'key' is not exist.'''
        idx = bisect.bisect_left(self._data, self._Item(key, None))
        if idx == len(self) or self._data[idx]._key != key:
            raise KeyError(f"{repr(key)} not found.")
        self._data.pop(idx)

    def __iter__(self):
        # Override MapBase (MutableMapping) ABC
        for item in self._data:
            yield item._key

    def __len__(self):
        # Override MapBase (MutableMapping) ABC
        return len(self._data) 

    def __repr__(self):
        return repr([x for x in self.items()])

    def __reversed__(self):
        for item in reversed(self._data):
            yield item._key

    def __str__(self):
        return str({x:y for x,y in self.items()})

    def find_range(self, start_key, stop_key = None):
        '''Find a range of key-value pairs in this ordered set where keys fit
        within right-open interval [start_key, stop_key). If start_key and 
        stop_key are None, entire key-value pairs will be traversed.
        '''
        idx = 0
        if start_key is not None or not isinstance(start_key, object):
            idx = bisect.bisect_left(self._data, self._Item(start_key, None))
        while idx < len(self) and \
                (self._data[idx]._key < stop_key or stop_key is None):
           yield self._data[idx] 
           idx += 1


# Much of our implementation here mirrors that of PriorityQueue ADT.
# Given that much of our functions are O(n) time, we will want to consider
# hashing functions to speed out our operational time. Even then, we see that
# Dictionaries are inherantly a little slower than some aspect of List.

class UnsortedMap(MapBase):
    '''Basic, concrete implementation of unsorted Maps (dictionary) ADT.'''
    def __init__(self):
        self._data = list()

    def __getitem__(self, key):
        # Override MapBase (MutableMapping) ABC
        '''Get item by 'key'. Raise KeyError if 'key' is not exist.
        O(n) time operation.
        '''
        for item in self._data:
            if key == item._key:
                return item._value
        raise KeyError(f"{repr(key)} not found.")

    def __setitem__(self, key, value):
        # Override MapBase (MutableMapping) ABC
        '''Set key-value pairs.
        Value associated with 'key' will be updated if item already exists.
        O(n) time operation.
        '''
        for item in self._data:
            if key == item._key:
                item._value = value
                return
        self._data.append(self._Item(key, value))

    def __delitem__(self, key):
        # Override MapBase (MutableMapping) ABC
        '''Delete Item by 'key'. Raise KeyError if 'key' is not exist.
        O(n) time operation.
        '''
        for idx in range(len(self)):
            if key == self._data[idx]._key:
                self._data.pop(idx)
                return
        raise KeyError(f"{repr(key)} not found.")

    def __iter__(self):
        # Override MapBase (MutableMapping) ABC
        for item in self._data:
            yield item._key

    def __len__(self):
        # Override MapBase (MutableMapping) ABC
        return len(self._data) 

    def __repr__(self):
        return repr([x for x in self.items()])

    def __reversed__(self):
        for item in reversed(self._data):
            yield item._key

    def __str__(self):
        return str({x:y for x,y in self.items()})
