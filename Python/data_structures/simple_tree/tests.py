#env python

from random import randrange, seed
from LinkedBinaryTree import LinkedBinaryTree

def test_case_bfs_tree():
    L = [_ for _ in range(100, 220, 10)]
    T = LinkedBinaryTree()
    T.build_bfs_tree(L)
    out_bfs = tuple(_ for _ in T.traverse_breadth_first())
    out_inorder = tuple(_ for _ in T.traverse_inorder())
    out_preorder = tuple(_ for _ in T.traverse_preorder())
    out_postorder = tuple(_ for _ in T.traverse_postorder())
    print(f"Original List: {L}")
    print(f"BFS Order: {out_bfs}")
    print(f"Inorder: {out_inorder}")
    print(f"Preorder: {out_preorder}")
    print(f"Postorder: {out_postorder}")
    print(f"Total Nodes: {len(T)}")
    print(f"Tree Height: {T.height()}")
    print()

def test_case_bst():
    L = [randrange(10, 99) for _ in range(12)]
    T = LinkedBinaryTree()
    T.build_bst(L)
    out_bfs = tuple(_ for _ in T.traverse_breadth_first())
    out_inorder = tuple(_ for _ in T.traverse_inorder())
    out_preorder = tuple(_ for _ in T.traverse_preorder())
    out_postorder = tuple(_ for _ in T.traverse_postorder())
    print(f"Original List: {L}")
    print(f"BFS Order: {out_bfs}")
    print(f"Inorder: {out_inorder}")
    print(f"Preorder: {out_preorder}")
    print(f"Postorder: {out_postorder}")
    print(f"Total Nodes: {len(T)}")
    print(f"Tree Height: {T.height()}")
    print()

def test_case_bfs2():
    # Can't do build_bst() on this kind of list unless we flatten L... or 
    # modify build_bst()
    L = ["calculus", ["analysis", "algebra"], "numerical", "field", "galois"]
    T = LinkedBinaryTree()
    T.build_bfs_tree(L)
    out_bfs = tuple(_ for _ in T.traverse_breadth_first())
    out_inorder = tuple(_ for _ in T.traverse_inorder())
    out_preorder = tuple(_ for _ in T.traverse_preorder())
    out_postorder = tuple(_ for _ in T.traverse_postorder())
    print(f"Original List: {L}")
    print(f"BFS Order: {out_bfs}")
    print(f"Inorder: {out_inorder}")
    print(f"Preorder: {out_preorder}")
    print(f"Postorder: {out_postorder}")
    print()


if __name__ == "__main__":
    test_case_bfs_tree()
    test_case_bst()
    test_case_bfs2()
