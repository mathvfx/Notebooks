#!env python

from ADT_Queue import ArrayQueue, LinkedQueue
from ADT_Stack import ArrayStack

    
def test_ArrayStack():
    print("~~~~~~~~~~~~~~~ Testing basic stack operations ~~~~~~~~~~~~~~~")
    S = ArrayStack()
    S.push(10)
    S.push(20)
    S.push(30)
    print(S)
    print(f"S.pop(): {S.pop()}")
    S.push(40)
    S += 100
    print(f"S.top(): {S.top()}")
    S.push(50)
    print(f"Current stack length: {len(S)}")
    print(S)
    print()

def test_ArrayQueue():
    print("~~~~~~~~~~~~~~~ Testing ArrayQueue ADT ~~~~~~~~~~~~~~~")
    L = [300, 500, 700]
    Q = ArrayQueue(L)
    Q.enqueue(10)
    Q.enqueue(20)
    Q.enqueue(30)
    print(Q)
    print(f"Q.dequeue(): {Q.dequeue()}")
    Q.enqueue(40)
    Q += 100
    print(f"Q.first(): {Q.first()}")
    Q.enqueue(50)
    print(f"Current Queue Length: {len(Q)}")
    Q.dequeue()
    Q.dequeue()
    Q.enqueue(1000)
    Q.enqueue(2000)
    print(Q)
    Q.reverse()
    print(Q)
    Q.enqueue(9)
    print(f"Q.first(): {Q.first()}")
    print(f"Q.dequeue(): {Q.dequeue()}")
    print(Q)
    print()

def test_LinkedQueue():
    print("~~~~~~~~~~~~~~~ Testing LinkedQueue ADT ~~~~~~~~~~~~~~~") 
    L = [300, 500, 700]
    Q = LinkedQueue(L)
    Q.enqueue(10)
    Q.enqueue(20)
    Q.enqueue(30)
    print(Q)
    print(f"Q.dequeue(): {Q.dequeue()}")
    Q.enqueue(40)
    Q += 100
    print(f"Q.first(): {Q.first()}")
    Q.enqueue(50)
    print(f"Current Queue Length: {len(Q)}")
    Q.dequeue()
    Q.dequeue()
    Q.enqueue(1000)
    Q.enqueue(2000)
    print(Q)
    Q.reverse()
    print(Q)
    Q.enqueue(9)
    print(f"Q.first(): {Q.first()}")
    print(f"Q.dequeue(): {Q.dequeue()}")
    print(Q)
    print()

if __name__ == "__main__":
    test_ArrayStack()
    test_ArrayQueue()
    test_LinkedQueue()
