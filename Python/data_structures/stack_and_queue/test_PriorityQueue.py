#!env python

from ADT_PriorityQueue import PriorityQueue
from random import randrange, choice

def test_HeapPQ():
    print("\n=================== Testing Priority Queue ===================\n")
    letters = "ABCDEFGHIJKLMNPQRSTUVWXYZ"
    L = [(randrange(10, 99), choice(letters)) for _ in range(10)]
    PQ = PriorityQueue()
    print(f"PQ empty? {PQ.is_empty()}")
    for x in L:
        PQ.add(*x)
    print(f"PQ still empty? {PQ.is_empty()}")
    print(f"PQ Height: {PQ.height()}")
    print(f"PQ Length: {len(PQ)}")
    print(f"PQ ORIGINAL: {PQ}\n")
    print(f"PEEK: {PQ.peek()}")
    print(f"PQ.add(95,'Z') {PQ.add(95, 'Z')}")
    print(f"PQ.add(5,'A') {PQ.add(5, 'A')}")
    print(f"PQ.add(5,'C') {PQ.add(5, 'C')}")
    print(f"PQ UPDATED: {PQ}\n")
    print(f"PQ.pop() = {PQ.pop()}")
    print(f"PQ changed: {PQ}\n")
    print(f"PQ.pop() = {PQ.pop()}")
    print(f"PQ.pop() = {PQ.pop()}")
    print(f"PQ.pop() = {PQ.pop()}")
    print(f"PQ.pop() = {PQ.pop()}")
    print(f"PQ changed: {PQ}\n")
    print(f"PQ contain 'Z'? {'Z' in PQ}")
    print(f"PQ contain 'O'? {'O' in PQ}")
    item = PQ.peek()
    print(f"PEEKed item is now: {item}")
    print(f"type(item) = {type(item)}")
    print(f"item.priority() = {item.priority()}")
    print(f"item.element() = {item.element()}")


if __name__ == "__main__":
    test_HeapPQ()
    
