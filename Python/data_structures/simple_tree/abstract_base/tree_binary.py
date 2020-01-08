#!env python
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises. 
#
# REFERENCES and CREDITS: 
#   Goodrich et al, DATA STRUCTURES AND ALGORITHMS IN PYTHON (2013), Wiley

from abc import abstractmethod
from .tree import Tree

class BinaryTree(Tree):
    '''Binary Tree ABC'''
    @abstractmethod
    def left_child(self, p: Tree.Position) -> Tree.Position:
        ...

    @abstractmethod
    def right_child(self, p: Tree.Position) -> Tree.Position:
        ...

    def sibling(self, p: Tree.Position) -> Tree.Position:
        '''Return Position of p's sibling.
           If p is a left child, then sibling(p) return right child vice versa.
           Root node has no siblings.
        '''
        parent = self.parent(p) 
        if parent is None:
            # Check for case of root node
            return None
        else:
            if self.left_child(parent) == p:
                return self.right_child(parent)
            else:
                return self.left_child(parent)

    def children(self, p: Tree.Position) -> iter:
        '''Override Tree ABC.
           Generate an iteration of Position p's children.
        '''
        if self.left_child(p) is not None:
            yield self.left_child(p)
        if self.right_child(p) is not None:
            yield self.right_child(p)
