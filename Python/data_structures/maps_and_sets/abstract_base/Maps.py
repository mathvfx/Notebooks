#env python3
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises. 
#
# REFERENCES and CREDITS: 
#   Goodrich et al, DATA STRUCTURES AND ALGORITHMS IN PYTHON (2013), Wiley


from collections.abc import MutableMapping


# By this point, we will instead utilize existing ABC from Python's ABC
# collections instead of rolling our own. We will implement Item container in 
# the same manner as our PriorityQueue ADT in stack_and_queue.
#
# Check Python's Docs for list of abstract method that needs to be implemented
# and methods (mixin) that have been included.


class MapBase(MutableMapping):
    '''MapBase ABC utilizing Python's MutableMapping and Mapping ABC.'''
    class _Item:
        __slots__ = ("_key", "_value")

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __eq__(self, other):
            '''Compare order of Item by key'''
            return self._key == other._key

        def __ge__(self, other):
            '''Compare order of Item by key'''
            return self._key >= other._key

        def __gt__(self, other):
            '''Compare order of Item by key'''
            return self._key > other._key

        def __le__(self, other):
            '''Compare order of Item by key'''
            return self._key <= other._key

        def __lt__(self, other):
            '''Compare order of Item by key'''
            return self._key < other._key

        def __ne__(self, other):
            '''Compare order of Item by key'''
            return not (self == other)

        def __str__(self):
            return str((self._key, self._value))

        def __repr__(self):
            return repr((self._key, self._value))

        def key(self):
            return self._key

        def value(self):
            return self._value
