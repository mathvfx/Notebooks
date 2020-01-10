#!env python
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises. 
#
# REFERENCES and CREDITS: 
#   Goodrich et al, DATA STRUCTURES AND ALGORITHMS IN PYTHON (2013), Wiley


from abstract_base.PriorityQueue import PQBase
from ADT_ArrayBinaryTree import ArrayBinaryTree

class Empty(Exception): 
    pass


# Don't forget about MRO issue for multiple inheritance
class PriorityQueue(ArrayBinaryTree, PQBase):
    '''An array-based binary (min) heap implementation of Priority Queue ADT.
    Min-heap order and complete binary heap properties are preserved. Output
    of Priority Queue will be in sorted order by priority value.
    '''
    def __init__(self, item_list: tuple = None):
        super().__init__()
        if item_list:
            self._heapify(item_list)

    def __contains__(self, elem):
        # Override PQBase ABC
        '''Return True if element is contained in this PQ.'''
        return any(x for x in self._data if elem == x.element())

    def __len__(self):
        # Override PQBase ABC
        return super().__len__()

    #TODO
    def __next__(self):
        # Override PQBase ABC
        pass

    def add(self, priority, elem):
        # Override PQBase ABC
        '''Push an element with its priority as Item into priority queue.
        "priority" element may be numerical value or objects that can be 
        compared. Smallest priority in PQ is the minimum of the set.
        '''
        super().add(self._Item(priority, elem))
        self._upheap(len(self) - 1)  # bubble-up for min-heap when adding item

    #TODO
    def merge(self, other):
        # Override PQBase ABC
        '''Merging other PQ into current PQ.'''
        pass

    def peek(self) -> PQBase._Item:
        # Override PQBase ABC
        '''Return (but not remove) top-priority Item from PQ. "Top-priority" is
        defined as Item with the smallest nonnegative priority number.
        '''
        if self.is_empty():
            raise Empty("PQ is empty. Cannot peek.")
        return self._data[0]   # type is _Item

    def pop(self) -> PQBase._Item:
        # Override PQBase ABC
        '''Remove and return top-priority Item from PQ. "Top-priority" is
        defined as Item with the smallest nonnegative priority number.
        '''
        if self.is_empty():
            raise Empty("PQ is empty. Cannot pop.")
        # Always maintain Complete Binary Tree Property first before fixing
        # Heap Order Property.
        self.swap(0, len(self)-1)   # move min root to the end node
        ans = self._data.pop()   # using Python's list.pop()
        self._downheap(0)   # Bubble-down for min-heap when removing item
        return ans

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Private utility functions

    def _upheap(self, idx: int):
        '''Bubble a node up the binary heap until Min Heap Order Property is
        satisfied.'''
        assert idx >= 0
        parent = self.parent(idx)
        if idx > 0 and self._data[idx] < self._data[parent]:
            self.swap(idx, parent)
            self._upheap(parent)

    def _downheap(self, idx: int):
        '''Bubble a node down the binary heap until Min Heap Order Property is
        satisfied.'''
        assert idx >= 0
        # Check first if last index is left-child within data length.
        # If it is, we still need to check for right-child in at index and 
        # compare smaller value in order to confirm smallest children. Finally,
        # we compare smallest child value to its parent and bubble down via
        # swap if smaller.
        if self.has_left_child(idx): 
            left = self.left_child(idx)
            min_child = left
            if self.has_right_child(idx):
                right = self.right_child(idx)
                if self._data[right] < self._data[left]:
                    min_child = right
            if self._data[min_child] < self._data[idx]:
                self.swap(idx, min_child)
                self._downheap(min_child)

    def _heapify(self, kv_list):
        '''Bottom-up approach to building binary heap from a given list of
        key-value pairs. O(n) operations, compared to otherwise O(n log n) time
        building from top-down.
        '''
        if self.is_empty():
            self._data = [self._Item(k, v) for k,v in kv_list]
            if len(self) > 1:
                start = self.parent(len(self) - 1)   # begin from last node
                for idx in range(start, -1, -1):
                    self._downheap(idx)
