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
class HeapPQ(ArrayBinaryTree, PQBase):
    '''An array-based binary (min) heap implementation of Priority Queue ADT.
    Min-heap order and complete binary heap properties are preserved.  

    NOTE: Priority value for each Item in HeapPQ is unique.
    '''
    #TODO: build heap from list
    def __init__(self, build_list: list = None):
        super().__init__()
    
    #TODO
    def __contains__(self, elem):
        # Override PQBase ABC
        pass

    def __len__(self):
        # Override PQBase ABC
        return super().__len__()

    #TODO
    def __next__(self):
        # Override PQBase ABC
        pass

    def add(self, key, elem):
        # Override PQBase ABC
        super().add(self._Item(key, elem))
        self._upheap(len(self) - 1)  # bubble-up for min-hip when adding item

    #TODO
    def merge(self, other):
        # Override PQBase ABC
        pass

    def peek(self) -> PQBase._Item:
        # Override PQBase ABC
        '''Return (but not remove) top-priority Item from PQ. "Top-priority" is
        is defined as Item with the smallest nonnegative priority number.
        '''
        if self.is_empty():
            raise Empty("PQ is empty. Cannot peak.")
        return self._data[0]   # type is _Item

    def pop(self) -> PQBase._Item:
        # Override PQBase ABC
        '''Remove and return top-priority Item from PQ. "Top-priority" is
        is defined as Item with the smallest nonnegative priority number.
        '''
        if self.is_empty():
            raise Empty("PQ is empty. Cannot peak.")
        self.swap(0, len(self)-1)   # move min root to the end node
        ans = self._data.pop()   # Python's list.pop()
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

if __name__ == "__main__":
    pq = HeapPQ()
    print(len(pq))
    print(pq.is_empty())
    pq.add(6, "Z")
    pq.add(12, "H")
    pq.add(16, "X")
    pq.add(5, "A")
    pq.add(7, "Q")
    pq.add(15, "K")
    pq.add(9, "F")
    pq.add(4, "C")
    pq.add(20, "B")
    pq.add(14, "E")
    pq.add(8, "W")
    pq.add(25, "J")
    pq.add(11, "S")
    print(pq.is_empty())
    item = pq.peek()
    print(type(item))
    print(item.priority())
    print(item.element())
    print(item)
    print(pq)
    print(f"height of this binary heap: {pq.height()}")
    print(pq.pop())
    print(pq.pop())
    item = pq.pop()
    print(type(item), item)
    print(pq)
