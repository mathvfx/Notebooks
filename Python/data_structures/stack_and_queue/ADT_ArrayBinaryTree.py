#!env python
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises. 
#
# REFERENCES and CREDITS: 
#   Goodrich et al, DATA STRUCTURES AND ALGORITHMS IN PYTHON (2013), Wiley

from math import floor, log

class ArrayBinaryTree:
    '''ArrayBinaryTree ADT is an array-based representation of a binary tree
    implemented using Python List as its underlying data storage. This is a 
    breadth-first (level) order binary tree and elements are unsorted.
    '''
    def __init__(self):
        self._data = list()

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return str(self._data)

    def add(self, elem):
        self._data.append(elem)

    def parent(self, idx: int) -> int:
        '''Bijective map between array index and binary tree parent node.
        Required idx >= 0. Return array index of parent node at idx.
        '''
        assert idx >= 0
        return (idx - 1)//2

    def left_child(self, idx: int) -> int:
        '''Bijective map between array index and binary tree left child node.
        Required idx >= 0. Return array index of left child node at idx.
        '''
        assert idx >= 0
        return 2*idx + 1

    def right_child(self, idx: int) -> int:
        '''Bijective map between array index and binary tree right child node.
        Required idx >= 0. Return array index of right child node at idx.
        '''
        assert idx >= 0
        return 2*idx + 2

    def has_left_child(self, idx: int) -> bool:
        '''Return True if last node in binary heap is a left-child.
        Required idx >= 0.
        '''
        assert idx >= 0
        return self.left_child(idx) < len(self)
        
    def has_right_child(self, idx: int) -> bool:
        '''Return True if last node in binary heap is a right-child.
        Required idx >= 0.
        '''
        assert idx >= 0
        return self.right_child(idx) < len(self)
    
    def height(self, n: int = -1) -> int:
        '''Return the height of index n of this level-order binary tree.
        By default, height() return the height of this entire tree.
        '''
        n = len(self) if n < 0 else n
        return floor(log(n+1)/log(2))

    def swap(self, i: int, j: int):
        assert i >= 0 and j >= 0
        self._data[i], self._data[j] = self._data[j], self._data[i]
