#!env python
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises. 
#
# REFERENCES and CREDITS: 
#   Goodrich et al, DATA STRUCTURES AND ALGORITHMS IN PYTHON (2013), Wiley

from abc import ABCMeta, abstractmethod

class Tree(metaclass=ABCMeta):
    '''General Tree ABC utilizing Position ABC.'''
    class Position:
        @abstractmethod
        def element(self):
            '''Return element at Position'''
    
        @abstractmethod
        def __eq__(self, other):
            ...
    
        def __ne__(self, other):
            return not (self == other)
    
    @abstractmethod
    def root(self) -> Position:
        '''Return Position of root node'''

    @abstractmethod
    def parent(self, p: Position) -> Position:
        '''Return Position parent of node p'''

    @abstractmethod
    def num_children(self, p: Position) -> int:
        '''Return total number of children of node p'''

    @abstractmethod
    def children(self, p: Position) -> iter:
        '''Return Iteration of Position for children of node p'''

    @abstractmethod
    def __len__(self) -> int:
        '''Return total number of nodes in this tree'''

    def is_root(self, p: Position) -> bool:
        return self.root() == p

    def is_leaf(self, p: Position) -> bool:
        return self.num_children(p) == 0

    def is_empty(self) -> bool:
        return len(self) == 0
        
    #~~~~~~~~~~~~~~~~~~~~~ Convenient tools for Trees ~~~~~~~~~~~~~~~~~~~~~~~~~

    def depth(self, p: Position) -> int:
        '''Return the number of levels seperating Position p from the root.
           One only needs to traverse up the parent until we hit the roots to 
           find such number.

           Note depth and level is similar, but not exactly same.
        '''
        if self.root():
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    def height(self, p: Position = None) -> int:
        '''Return the max height of current subtree rooted at Position p. '''
        def _height(p: self.Position) -> int:
            '''Traverse to farthest leaf from current position p recursively'''
            if self.is_leaf(p):
                return 0
            else:
                return 1 + max(_height(p) for p in self.children(p))

        if p is None:
            # Allows us to get height of entire tree rather than just subtree
            p = self.root()
        return _height(p)


# Note that general Tree ABC only has Accessors and no Mutators.
# Mutators will be implemented in concrete classes. We may not want such 
# mutators to be public interface because some form of mutator may be suitable
# for one class and not for others.

# Using Position ABC allows for greater generalization of Tree. For example,
# We can implement subclass it into general m-ary tree, or binary tree using
# Linked List or Array. 
