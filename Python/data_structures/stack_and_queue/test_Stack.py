#!env python

from ADT_Stack import ArrayStack, LinkedStack

    
def test_ArrayStack():
    print(" >> Testing ArrayStack ADT")
    L = [333, 444, 555]
    print(f" >> Build ArrayStack and initialize with {L}")
    S = ArrayStack(L)
    print(" >> Pushing 10, 20, 30")
    S.push(10)
    S.push(20)
    S.push(30)
    print(S)
    print(f"S.pop(): {S.pop()}")
    print(" >> Pushing 40, and __iadd__ 100")
    S.push(40)
    S += 100
    print(f"S.top(): {S.top()}")
    print(" >> Pushing 50")
    S.push(50)
    print(f"Current stack length: {len(S)}")
    print(S)
    print(f"Does S contains 555? {555 in S}")
    print(f"Does S contains 556? {556 in S}")
    print(f"Which index is is 555? {S.index(555)}")
    print(f"Which index is is 556? {S.index(556)}")
    print("...now reverse this stack")
    S.reverse()
    print(" >> push 50")
    S.push(50)
    print(S)
    print(f"Occurrences of 50? {S.count(50)}")
    print(f"Occurrences of 51? {S.count(51)}")
    print()

def test_LinkedStack():
    print(" >> Testing LinkedStack ADT") 
    L = [333, 444, 555]
    print(f" >> Build LinkedStack and initialize with {L}")
    S = LinkedStack(L)
    print(" >> Pushing 10, 20, 30")
    S.push(10)
    S.push(20)
    S.push(30)
    print(S)
    print(f"S.pop(): {S.pop()}")
    print(" >> Pushing 40, and __iadd__ 100")
    S.push(40)
    S += 100
    print(f"S.top(): {S.top()}")
    print(" >> Pushing 50")
    S.push(50)
    print(f"Current stack length: {len(S)}")
    print(S)
    print(f"Does S contains 555? {555 in S}")
    print(f"Does S contains 556? {556 in S}")
    print(f"Which index is is 555? {S.index(555)}")
    print(f"Which index is is 556? {S.index(556)}")
    print("...now reverse this stack")
    S.reverse()
    print(" >> push 50")
    S.push(50)
    print(S)
    print(f"Occurrences of 50? {S.count(50)}")
    print(f"Occurrences of 51? {S.count(51)}")
    print()


if __name__ == "__main__":
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    test_ArrayStack()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    test_LinkedStack()
