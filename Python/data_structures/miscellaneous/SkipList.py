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
#
# Skip List really is an interesting data structure in that it utilizes
# probabilistic model to obtain an average of order log n search time. However, 
# this come at the expense of order n log n space requirments. In other words,
# suppose we have n = 1 million elements, we can expect an average of 42 steps 
# to reach solution. However, this performance speed may come at a cost of an 
# average of 2 million elements to be stored in memory. Therefore, Skip List 
# may not be ideal for system with tight memory constraint.
#
# Although we can implement Skip List using Python's list of lists, but the
# cost of O(n log n) may not be worth it for List, since binary search may
# suffice. Instead, for exercise, I implemented it as a singly linked-list of
# list--- where each node will contain actual element and a list of references 
# to the next node. Keeping in mind that Python List still has amortization
# costs in its storage compared having each linked node containing an element
# and 3 references. (Still it is a trade-off)
#
# Skip List will require users to consider space vs. time trade-off.


from abstract_base.SKBase import SkipListBase


class SkipList(SkipListBase):
    '''Skip List is a probabilistic data structure containing sorted elements.

       This implementation is an O(n) time operation with average O(log n) and 
       requiring O(n log n) space.
    '''
    def find_min(self) -> object:
        '''Return the smallest element in Skip List.'''
        return self._header[0].element()

    def find_max(self) -> object:
        '''Return the largest element in Skip List.'''
        node = self._header
        for h in range(self._max_level, -1, -1):
            while node[h]:
                node = node[h]
        return node.element()

    def find_range(self, elem_min, elem_max) -> list:
        '''Return a list of element in the interval [elem_min, elem_max].'''
        assert elem_min <= elem_max
        node_list = list()
        min_node = self._search_node(elem_min)
        if min_node.element() == elem_min:
            node_list.append(min_node.element())
        max_node = self._search_node(elem_max)
        walk = min_node
        while walk.element() < max_node.element():
            walk = walk[0]
            node_list.append(walk.element())
        return node_list
        
    def find_nearest(self, elem) -> object:
        '''Return the largest element that is smaller than or equal to "elem".
        '''
        node = self._search_node(elem)
        return node.element()

    def path_to_target(self, elem) -> list:
        '''Return a list of traversed elements as we find "elem". Path traversed
        is randomized. This method can be used to observe Skip List traversal.
        '''
        return self._search_node_path(elem)
    
    def pop(self, elem=None) -> object:
        '''Return and remove "elem" from Skip List. If input is not specified,
        last element will be popped instead.
        '''
        if elem is None:
            elem = self.find_max()
        ans = self._remove_node(elem)
        return ans

    def push(self, elem):
        '''Push an element into Skip List.'''
        self._insert_node(elem)
