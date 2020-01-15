#!env python3

from ADT_ArrayBinaryTree import ArrayBinaryTree

#TODO: Optimize and clean up this messy code
def heapsort(build_list: list):
    '''Heapsort a given list.

    We first heapify a list using same idea from downheap and heapify methods 
    adapted from our ADT_PriorityQueue. Likewise, we still use the same
    downheap method to preserve max-heap ordering and complete binary heap 
    properties-- but on shrinking list of iteams.

    Without spending too much time, we're looking at O(n) storage usage
    (because we didn't re-use our original heap list), with O(n log n) time.

    This code should probably be further optimized at some point.
    '''
    def _downheap(L: ArrayBinaryTree, idx: int):
        if L.has_left_child(idx):
            left = L.left_child(idx)
            max_child = left
            if L.has_right_child(idx):
                right = L.right_child(idx)
                if L[right] > L[left]:
                    max_child = right
            if L[max_child] > L[idx]:
                L.swap(idx, max_child)
                _downheap(L, max_child)

    # Phase 1: Heapify a list.
    my_heap = ArrayBinaryTree(build_list)
    count = len(my_heap)
    if count > 1:
        start = my_heap.parent(count-1)
        for idx in range(start, -1, -1):
            _downheap(my_heap, idx)

    # Phase 2: Heap-Sort the array by progressively shrinking downheap list
    new_list = [None]*count
    while count > 0:
        my_heap.swap(0, count-1) # move roots to the last entry
        new_list[count-1] = my_heap.pop()
        _downheap(my_heap, 0)
        count -= 1

    return new_list

    
if __name__ == "__main__":
    from random import randrange
    L = [randrange(100, 900) for _ in range(10)]
    print(f"  Original List: {L}")
    print(f"Heapsorted List: {heapsort(L)}")
