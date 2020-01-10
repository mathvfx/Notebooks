#!env python

from ADT_Deque import LinkedDeque

def test_LinkedDeque():
    print(" >> Test LinkedDeque ADT")
    L = [300, 500, 700]
    print(f" >> Build LinkedDeque and initialize with {L}")
    D = LinkedDeque(L)
    print(" >> enqueue 10, 20, 30")
    D.enqueue(10)
    D.enqueue(20)
    D.enqueue(30)
    print(" >> enqueue_back -10, -20")
    D.enqueue_back(-10)
    D.enqueue_back(-20)
    print(D)
    print(f"D.dequeue(): {D.dequeue()}")
    print(f"D.dequeue_back(): {D.dequeue_back()}")
    print(D)
    print(f"D.front(): {D.front()}")
    print(f"D.back(): {D.back()}")
    print(f"Does D contains 700? {700 in D}")
    print(f"Does D contains 702? {702 in D}")
    D.enqueue(777)
    print(D)
    D.rotate(3)
    print(D)
    D.reverse()
    print(" >> enqueue 300")
    D.enqueue(300)
    print(D)
    print(f"Occurrences of 300? {D.count(300)}")
    print(f"Occurrences of 301? {D.count(301)}")
    print()

if __name__ == "__main__":
    test_LinkedDeque()
