#!env python3
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises. 
#
# REFERENCES and CREDITS: 
#   Goodrich et al, DATA STRUCTURES AND ALGORITHMS IN PYTHON (2013), Wiley


from abstract_base.Maps import MapBase


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

    def __str__(self):
        return str([_ for _ in self._data])
