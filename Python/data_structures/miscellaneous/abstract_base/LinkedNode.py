#!env python3
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises. 


class SKNode:
    __slots__ = ("_elem", "_ref")

    def __init__(self, elem, next_ptr=None):
        self._elem = elem
        self._ref = [next_ptr]

    def __len__(self):
        '''Number of References.'''
        return len(self._ref)

    def __iter__(self):
        for link in self._ref:
            yield link

    def __delitem__(self, idx):
        self._ref.pop(idx)

    def __getitem__(self, idx):
        if idx >= len(self):
            return None
        return self._ref[idx]

    def __eq__(self, other_node):
        return self._elem == other_node._elem

    def __ge__(self, other_node):
        return self._elem >= other_node._elem

    def __gt__(self, other_node):
        return self._elem > other_node._elem

    def __le__(self, other_node):
        return self._elem <= other_node._elem

    def __lt__(self, other_node):
        return self._elem < other_node._elem

    def __ne__(self, other_node):
        return self._elem != other_node._elem

    def __setitem__(self, idx, node):
        self._ref[idx] = node

    def __repr__(self):
        return repr(self._elem)

    def __str__(self):
        return str(self._elem)

    def element(self):
        return self._elem
