#!env python
#
# Alex Lim. 2020. https://mathvfx.github.io
# This Python code is intended as my own learning and programming exercises. 
#
# REFERENCES and CREDITS: 
#   Goodrich et al, DATA STRUCTURES AND ALGORITHMS IN PYTHON (2013), Wiley

from abstract_base.Deque import DequeBase

class Empty(Exception):
    pass

# While we can consider ArrayDeque implementation, finding a bijective function
# that gives proper array indices can be a significant work. We will instead
# implement our Deque using doubly linked-list and leave ArrayDeque as an
# exercise for the reader. Or in the future.

class LinkedDeque(DequeBase):
    '''Simple LinkedDeque ADT implemented using doubly linked-list.
       Please consider collections.deque for production usage.
    '''
    class _Node:
        __slots__ = ("_elem", "_next", "_prev")
        def __init__(self, elem, prev=None, nxt=None):
            self._elem = elem
            self._next = nxt
            self._prev = prev

        def __str__(self):
            text = f"NODE<{id(self)}> "
            text += f":: PREV<{id(self._prev)}> :: NEXT<{id(self._next)}> "
            text += f":: ELEM({self._elem})"
            return text
        
        def element(self):
            return self._elem
        
    def __init__(self, build_list: list = None):
        '''LinkedDeque ADT constructor'''
        self._header = self._Node(None)                      # header sentinel
        self._trailer = self._Node(None, prev=self._header)  # trailer sentinel
        self._header._next = self._trailer
        self._size = 0
        if build_list:
            for elem in build_list:
                self.enqueue(elem)

    def __contains__(self, elem):
        # Override DEQue ABC
        '''Return True is Deque contains "elem". O(n) operation.'''
        walk = self._header._next
        while walk is not self._trailer:
            if elem == walk.element():
                return True
            walk = walk._next
        return False

    def __len__(self):
        # Override DEQue ABC
        return self._size

    def __str__(self):
        if self.is_empty():
            return " >> DEBUG LinkedDeque is empty."
        head = self._header._next
        node_list = [None] * len(self)
        for idx in range(len(self)):
            node_list[idx] = str(head.element())
            head = head._next
        return f" >> DEBUG LinkedDeque [{len(self)}]: *{', '.join(node_list)}"
    
    def back(self):
        # Override DEQue ABC
        '''Return the last dequeue (tail) element in the deque.'''
        if self.is_empty():
            # we don't return None because None may be a valid object
            raise empty("Deque is empty.")
        return self._trailer._prev._elem

    def count(self, elem) -> int:
        '''Return the number of occurrences of element "elem" in the deque.
           O(n) operations.
        '''
        walk = self._header._next
        ans = 0
        for _ in range(self._size):
            if walk.element() == elem:
                ans += 1
            walk = walk._next
        return ans

    def dequeue(self):
        # Override DEQue ABC
        '''Return and remove the front (head) element from the deque.'''
        if self.is_empty():
            raise empty("Deque is empty. Cannot pop_back.")
        return self._remove(self._header._next)

    def dequeue_back(self):
        # Override DEQue ABC
        '''Return and remove the back (tail) element from the deque.'''
        if self.is_empty():
            raise empty("Deque is empty. Cannot pop_front.")
        return self._remove(self._trailer._prev)

    def enqueue(self, elem):
        # Override DEQue ABC
        '''Append element "elem" to the back (tail) of the deque.'''
        self._insert(elem, prev=self._trailer._prev, nxt=self._trailer)

    def enqueue_back(self, elem):
        # Override DEQue ABC
        '''Append element "elem" to the front (head) of the deque.'''
        self._insert(elem, prev=self._header, nxt=self._header._next)

    def front(self):
        # Override DEQue ABC
        '''Return the next dequeue (head) element in the deque.'''
        if self.is_empty():
            # we don't return None because None may be a valid object
            raise empty("Deque is empty.")
        return self._header._next._elem
    
    #TODO
    def remove(self, elem, index: int = -1):
        '''Remove element "elem" nearest to the front of the queue.
           If 0 <= index <= len(queue), item positioned at that index is
           removed. O(n) operations.
        '''
        pass

    def reverse(self):
        # Override DEQue ABC
        '''Reverse deque in-place.'''
        if self.is_empty():
            raise Empty("Deque is empty.")
        if self._size > 1:
            head = self._header._next
            tail = self._trailer._prev
            for _ in range(self._size//2):
                head._elem, tail._elem = tail._elem, head._elem
                head = head._next
                tail = tail._prev

    def rotate(self, n: int = 1):
        '''Rotate deque by n steps to the right if n > 0, to the left if n < 0.
           No rotate action if n = 0. O(n) operations and memory.
        '''
        if self.is_empty():
            raise Empty("Queue is empty.")
        if self._size > 1 and n != 0:   
            if n > 0:   # rightward rotation
                direction = "_next"
                sentinel = self._header
                guard = self._trailer
            elif n < 0:   # leftward rotation
                direction = "_prev"
                sentinel = self._trailer
                guard = self._header
                n *= -1   # ensure n > 0 for position modulus
            head = getattr(sentinel, direction)
            queue_items = [head._elem]
            for _ in range(n % len(self)):   # moving to nth position to begin
                head = getattr(head, direction)
                queue_items.append(head._elem)
            for _ in range(len(self)):   # start rotate operations
                head._elem = queue_items.pop(0)
                if getattr(head, direction) is not guard:
                    head = getattr(head, direction)
                else:   # reached last sentinel, so cycle back to first
                    head = getattr(sentinel, direction)
                queue_items.append(head._elem)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Private helper methods

    def _insert(self, elem, prev: _Node, nxt: _Node):
        '''Insert elements between "prev" and "nxt" nodes'''
        new_node = self._Node(elem, prev, nxt)
        prev._next = new_node
        nxt._prev = new_node
        self._size += 1
        return new_node
    
    def _remove(self, node: _Node):
        '''Remove "node" from doubly linked-list and return node's element'''
        # Rewire current node
        node._prev._next = node._next  # update previous node's pointer to next
        node._next._prev = node._prev  # update next node's pointer to previous
        self._size -= 1

        # For aid with garbage collection
        ans = node._elem
        node._elem = node._prev = node._next = None
        return ans
