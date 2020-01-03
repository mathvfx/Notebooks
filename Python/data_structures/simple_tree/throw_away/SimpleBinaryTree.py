#!env python

class Node:
    __slots__ = ("_elem", "_parent", "_left", "_right")
    def __init__(self, elem, parent=None, left=None, right=None):
        self._elem = elem
        self._parent = parent
        self._left = left
        self._right = right
    
    def __str__(self):
        text = f"NODE({id(self)}) : ELEM({self._elem}) "
        text += f": LF({id(self._left)}), RT({id(self._right)}))"
        return text

    def element(self):
        return self._elem


class BinaryTree:
    def __init__(self):
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return len(self) == 0

    def root(self) -> Node:
        return self._root

    def parent(self, node: Node) -> Node:
        return node._parent

    def left_child(self, node: Node) -> Node:
        return node._left

    def right_child(self, node: Node) -> Node:
        return node._right

    def children(self, node: Node) -> Node:
        if node._left is not None:
            yield node._left
        if node._right is not None:
            yield node._right

    def sibling(self, node: Node) -> Node:
        parent = node._parent
        if parent is None:
            # We're at root
            return None
        else:
            if parent._left == node:
                return parent._right
            else:
                return parent._left

    def num_children(self, node: Node) -> int:
        count = 0
        if node._left is not None:
            count += 1
        if node._right is not None:
            count += 1
        return count

    def add_root(self, elem) -> Node:
        if self._root is not None:
            raise ValueError("Root already exist. Cannot add.")
        self._root = Node(elem)
        self._size = 1
        return self._root

    def add_left_child(self, node: Node, elem) -> Node:
        if node._left is not None:
            raise ValueError("Left child already exist. Cannot add.")
        node._left = Node(elem, parent=node)
        self._size += 1
        return node._left

    def add_right_child(self, node: Node, elem) -> Node:
        if node._right is not None:
            raise ValueError("Right child already exist. Cannot add.")
        node._right = Node(elem, parent=node)
        self._size += 1
        return node._right

    def build_bfs_tree(self, build_list: list):
        '''Build breadth-first (level) order binary tree data structure from 
           a given nonempty list. First entry of the list will be the root.
        '''
        assert len(build_list) > 0 # Temporary line. Lazy.
        L = build_list[::-1] # shallow copy in reverse
        root = self.add_root(L.pop())
        levels = [root]
        while True:
            node = levels.pop(0) # dequeue
            left_node = self.add_left_child(node, L.pop())
            if not L: break
            right_node = self.add_right_child(node, L.pop())
            if not L: break
            levels.extend([left_node, right_node]) # enqueue
        # The list 'levels' actually represents our queuing (deque) system.
        # dequeue operations would meant we're adding child node, while enqueue
        # represented adding subtree root node to be processed for that level.
        # The whole build process ends when we ran out of item in L rather 
        # than when deque is empty. Thus BFS and Deque are related, and 
        # DFS and Stack are related

    def build_bst(self, build_list: list):
        '''Build Binary Search Tree data structure from a given nonempty list.
           First entry of the list will be considered as root. Outcome is an
           In-Order binary tree.
        '''
        pass

    def traverse_preorder(self, node: Node = None) -> iter:
        '''Traverse Binary Tree in Pre-Order. Roughly speaking, visit root then
           all other children.
        '''
        def _pre(root):
            yield root.element()
            for c in self.children(root):
                for other in _pre(c):
                    yield other
        root = self._root if node is None else node
        if not self.is_empty():
            for p in _pre(root):
                yield p

    def traverse_postorder(self, node: Node = None) -> iter:
        '''Traverse Binary Tree in Post-Order. Roughly speaking, visit all 
           children then root.
        '''
        def _post(root):
            for c in self.children(root):
                for other in _post(c):
                    yield other
            yield root.element()
        root = self._root if node is None else node
        if not self.is_empty():
            for p in _post(root):
                yield p

    def traverse_inorder(self, node: Node = None) -> iter:
        '''Traverse Binary Tree in In-Order. Roughly speaking, visit left-most 
           child, then root, then remaining children.
        '''
        def _inorder(root):
            if self.left_child(root):
                for left in _inorder(self.left_child(root)):
                    yield left
            yield root.element()
            if self.right_child(root):
                for right in _inorder(self.right_child(root)):
                    yield right
        root = self._root if node is None else node
        for p in _inorder(root):
            yield p
    
    def traverse_breadth_first(self, node: Node = None) -> iter:
        '''Traverse Binary Tree in Breadth-First Search Order.'''
        root = self._root if node is None else node
        levels = [root] # deque
        while levels:
            node = levels.pop(0) # dequeue
            yield node.element() # visited
            for c in self.children(node):
                levels.append(c) # enqueue

    def traverse_depth_first(self, node: Node = None) -> iter:
        '''Traverse Binary Tree in Depth-First Search Order.'''
        pass


if __name__ == "__main__":
    L = [_ for _ in range(100, 220, 10)]
    T = BinaryTree()
    T.build_bfs_tree(L)
    out_inorder = tuple(_ for _ in T.traverse_inorder())
    out_preorder = tuple(_ for _ in T.traverse_preorder())
    out_postorder = tuple(_ for _ in T.traverse_postorder())
    out_bfs = tuple(_ for _ in T.traverse_breadth_first())
    print(f"Original List: {L}")
    print(f"BFS Order: {out_bfs}")
    print(f"Inorder: {out_inorder}")
    print(f"Preorder: {out_preorder}")
    print(f"Postorder: {out_postorder}")
    print(f"Total Nodes: {len(T)}")
