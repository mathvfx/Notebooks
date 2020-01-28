#!env python3
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises. 
#
# REFERENCES and CREDITS:
# 1. COMP2402 Fall 2016, Pat Morin, Carleton Univ. https://youtu.be/7pWkspmYUVo
# 2. Goodrich et al, DATA STRUCTURES AND ALGORITHMS IN PYTHON (2013), Wiley
# 3. Wikipedia contributors. "Skip list." Wikipedia, The Free Encyclopedia. 
#      Wikipedia, The Free Encyclopedia, 22 Dec. 2019. Web. 24 Jan. 2020.


import collections.abc as ABC
import random
from .LinkedNode import SKNode


class SkipListBase(ABC.Collection):
    _SENTINEL = object()

    def __init__(self, build_list: list = None):
        self._header = SKNode(self._SENTINEL)   # head sentinel
        self._max_level = 0
        self._size = 0
        if build_list:
            for elem in build_list:
                self._insert_node(SKNode(elem))

    def __add__(self, elem):
        if not isinstance(elem, SKNode):
            elem = SKNode(elem)
        self._insert_node(elem)
        return self

    def __contains__(self, elem):
        elem_node = SKNode(elem)
        return self._search_node(elem_node) == elem_node

    def __iadd__(self, elem):
        self.__add__(elem)
        return self

    def __iter__(self):
        walk = self._header[0]
        while walk:
            yield walk
            walk = walk[0]

    def __len__(self):
        '''Return the number of elements in this list.'''
        return self._size

    def __repr__(self):
        node_list = [None] * len(self)
        walk = self._header[0]
        for idx in range(len(self)):
            node_list[idx] = walk.element()
            walk = walk[0]
        return repr(node_list)

    def __str__(self):
        return f"SkipList: {self.__repr__()}"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #  Friend Methods

    def _insert_node(self, new_node: SKNode):
        '''Insert a new node into Skip List.
        Raise KeyError exception if "new_node" already exist.
        '''
        if not isinstance(new_node, SKNode):
            new_node = SKNode(new_node)
        curr_node = self._search_node(new_node)
        if curr_node == new_node:
            raise KeyError(f"{repr(new_node)} already exists in Skip List.")
        new_node[0] = curr_node[0]
        curr_node[0] = new_node
        self._size += 1
        level_idx = 1   # move up to next level to begin
        while random.random() < 0.5:   # uniform distribution
        #while random.gauss(0.5, 0.3) <= 0.5:
            if self._max_level >= level_idx:
                walk = self._header
                while walk[level_idx] and walk[level_idx] < new_node:
                    walk = walk[level_idx]   # horizontal walk
                new_node._ref.append(walk[level_idx])
                walk[level_idx] = new_node
            else:
                new_node._ref.append(None)
                self._header._ref.append(new_node)
                self._max_level += 1
            level_idx += 1   # vertical rise

    def _remove_node(self, node: SKNode) -> object:
        '''Remove a node from Skip List.
        Raise KeyError if "node" is not found.
        '''
        if not isinstance(node, SKNode):
            node = SKNode(node)
        target_node = self._search_node(node)
        if target_node != node:
            raise KeyError(f"{repr(node)} could not be found in Skip List.")
        walk = self._header
        for level_idx in range(len(target_node)-1, -1, -1):
            while walk[level_idx] and walk[level_idx] != target_node:
                walk = walk[level_idx]
            walk[level_idx] = target_node[level_idx]
            target_node[level_idx] = None   # aid garbage collection
            if self._header[level_idx] is None:
                self._header._ref.pop(level_idx)
        ans = target_node.element()
        target_node._elem = None   # aid garbage collection
        self._size -= 1
        return ans

    def _search_node(self, elem) -> SKNode:
        '''Search for node with "elem" element. If no "elem" is found, then
        return the maximal node that is less than "elem". It is possible also
        the return node is a sentinel node.
        '''
        if not isinstance(elem, SKNode):
            elem = SKNode(elem)
        node = self._header   # Starting node from the top
        for h in range(self._max_level, -1, -1):   # vertical drop
            while node[h] is not None and node[h] <= elem:
                node = node[h]   # horizontal walk
        return node   # may be max{node.element(), elem} 

    def _search_node_path(self, elem) -> list:
        '''Same as _search_node method, only this method will provide a list of
        nodes traversed.
        '''
        if not isinstance(elem, SKNode):
            elem = SKNode(elem)
        path_list = list()
        node = self._header
        for h in range(self._max_level, -1, -1): 
            while node[h] is not None and node[h] <= elem:
                node = node[h]
                path_list.append(node.element())
        return path_list
