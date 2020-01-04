#!env python

#TODO:
# 1. Implement node search
# 2. Subtree attachments
# 3. Code verification for correctness

from abstract_base.tree_binary import BinaryTree

class LinkedBinaryTree(BinaryTree):
    '''Simple Binary Tree implemented with Linked-List'''
    class Node:
        # NOTE 'self' here is Node container
        __slots__ = ("_parent", "_left", "_right", "_elem")
        def __init__(self, elem, parent=None, left=None, right=None):
            self._parent = parent
            self._left = left
            self._right = right
            self._elem = elem
        
        def __str__(self):
            text = f"NODE<{id(self)}>::LF<{id(self._left)}>::"
            text += f"RT<{id(self._right)}>::PAR<{id(self._parent)}> : "
            text += f"ELEM<{self._elem}>"
            return text

    class Position(BinaryTree.Position):
        # NOTE 'self' here is Position container
        __slots__ = ("_container", "_node")
        def __init__(self, container: BinaryTree.Position, node):
            self._container = container
            self._node = node

        def element(self) -> BinaryTree.Position:
            # Override Tree ABC
            return self._node._elem

        def __eq__(self, other: BinaryTree.Position):
            # Override Tree ABC
            # Equality here meant both types are the same type, 
            # and both node is the same node.
            return type(other) is type(self) and other._node is self._node

    def _position_to_node(self, p: Position) -> Node:
        '''Convert Position object to Node object'''
        if not isinstance(p, self.Position):
            raise TypeError('p must be of type Position')
        if p._container is not self:
            raise ValueError("p doesn't belong to this container")
        if p._node._parent is p._node: #invalidate for removed node
            raise ValueError("p has been removed and is no longer valid")
        return p._node

    def _node_to_position(self, node: Node) -> BinaryTree.Position:
        '''Convert Node object to Position object'''
        return self.Position(self, node) if node else None

    #--------------------------------------------------------------------------
    # Overrides Tree and BinaryTree ABC. These are Accessors.

    def __init__(self):
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size
        # Note this wasn't specified in Tree ABC because we don't know how 
        # "size" (length) will be defined there.

    def root(self) -> Position:
        # Override Tree ABC
        return self._node_to_position(self._root)

    def parent(self, p: Position) -> Position:
        # Override Tree ABC
        node = self._position_to_node(p)
        return self._node_to_position(node._parent)

    def left_child(self, p: Position) -> Position:
        # Override BinaryTree ABC
        node = self._position_to_node(p)
        return self._node_to_position(node._left)

    def right_child(self, p: Position) -> Position:
        # Override BinaryTree ABC
        node = self._position_to_node(p)
        return self._node_to_position(node._right)

    def num_children(self, p: Position) -> int:
        # Override Tree ABC
        # num_children will be 0, 1, or 2 for BinaryTree
        node = self._position_to_node(p)
        count = 0
        if node._left is not None:
            count += 1
        if node._right is not None:
            count += 1
        return count

    #--------------------------------------------------------------------------
    # Adding private Mutators specific to LinkedBinaryTree ADT

    def _add_root(self, elem) -> Position:
        if self._root is not None:
            raise ValueError("Root already exists. Cannot add.")
        self._size = 1
        self._root = self.Node(elem)
        return self._node_to_position(self._root)

    def _add_left_child(self, p: Position, elem) -> Position:
        node = self._position_to_node(p)
        if node._left is not None:
            raise ValueError("Left child already exist. Cannot add.")
        self._size += 1
        node._left = self.Node(elem, node)
        return self._node_to_position(node._left)

    def _add_right_child(self, p: Position, elem) -> Position: 
        node = self._position_to_node(p)
        if node._right is not None:
            raise ValueError("Right child already exist. Cannot add.")
        self._size += 1
        node._right = self.Node(elem, node)
        return self._node_to_position(node._right)

    def _replace(self, p: Position, elem):
        '''Replacing elements of a node in tree without changing position.
           
           Return p's original element.
        '''
        node = self._position_to_node(p)
        old = node._elem
        node._elem = elem
        return old

    def _delete(self, p: Position):
        '''Remove node Position p (with at most 1 child) from the tree.
           Restriction of "at most one child" is due to the fact that binary 
           tree cannot have more than two children for each node.

           Return p's element.
        '''
        node = self._position_to_node(p)
        if self.num_children(p) == 2:
            raise ValueError("p has two children. Cannot remove.")
        child = node._left if node._left else node._right # child could be None
        if child is not None:
            child._parent = node._parent # node._parent could be None
        if node is self._root: # root-node case
            self._root = child 
        else:  # leaf-node case
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node
        return node._elem

    def _attach(self, p: Position, t: BinaryTree):
        '''Attach BinaryTree t to node position p if child slot is available.
        '''
        node = self._position_to_node(p) # additional verifications within
        if self.num_chilren(p) > 1:
            raise ValueError('Position p have no available slot.')
        if not type(self) is type(t):
            raise TypeError("Tree types must match")
        self._size += len(t)
        if not t.is_empty():
            t._root._parent = node # attach tree t to current position p
            if node._left is None:
                node._left = t._root
            else:
                node._right = t._root
            # Tree t is no longer "has" root or size of its own
            t._root = None  
            t._size = 0    

    #--------------------------------------------------------------------------
    # Adding basic public methods for tree constructions and traversal

    def build_bfs_tree(self, build_list: list):
        '''Build Binary Tree data structure in breadth-first (level) order.
           First element of build_list is considered as root of the tree.
        '''
        assert len(build_list) > 0 # Temporary line. Lazy.
        L = build_list[::-1] # Shallow copy in reverse
        root = self._add_root(L.pop())
        levels = [root] # queue
        while len(L) > 0:
            node = levels.pop(0) # dequeue
            left_node = self._add_left_child(node, L.pop())
            if not L: break
            right_node = self._add_right_child(node, L.pop())
            if not L: break
            levels.extend([left_node, right_node]) #enqueue

    def build_bst(self, build_list: list):
        '''Build Binary Search Tree data struture.
           First element of build_list is considered as root of the tree.
        '''
        assert len(build_list) > 0 # Temporary line. Lazy.
        def _insert(pos, elem):
            if elem < pos.element(): # ascending. Change to > for desc. order
                if self.left_child(pos):
                    _insert(self.left_child(pos), elem)
                else:
                    self._add_left_child(pos, elem)
            else:
                if self.right_child(pos):
                    _insert(self.right_child(pos), elem)
                else:
                    self._add_right_child(pos, elem)
        root = self._add_root(build_list[0])
        for idx in range(1, len(build_list)):
            _insert(root, build_list[idx])

    def traverse_breadth_first(self, p: Position = None) -> iter:
        '''Breadth-first binary tree traversal starting from node Position p.
        '''
        root = self.root() if p is None else p
        levels = [root] # queue
        while levels:
            node = levels.pop(0) # dequeue
            yield node.element() # visited
            for c in self.children(node):
                levels.append(c) # enqueue

    def traverse_preorder(self, p: Position = None) -> iter:
        '''Depth-first binary tree traversal in pre-order starting from node p. 
           Roughly speaking, visit root then all other children.
        '''
        def _pre(root):
            yield root.element()
            for c in self.children(root):
                for other in _pre(c):
                    yield other
        root = self.root() if p is None else p
        if not self.is_empty():
            for position in _pre(root):
                yield position

    def traverse_postorder(self, p: Position = None) -> iter:
        '''Depth-first binary tree traversal in post-order starting from node p. 
           Roughly speaking, visit all children then root.
        '''
        def _post(root):
            for c in self.children(root):
                for other in _post(c):
                    yield other
            yield root.element()
        root = self.root() if p is None else p
        if not self.is_empty():
            for position in _post(root):
                yield position

    def traverse_inorder(self, p: Position = None) -> iter:
        '''Depth-first binary tree traversal in in-order starting from node p. 
           Roughly speaking, visit left-most child, then root, then remaining 
           children.
        '''
        def _inorder(root):
            if self.left_child(root):
                for left in _inorder(self.left_child(root)):
                    yield left
            yield root.element()
            if self.right_child(root):
                for right in _inorder(self.right_child(root)):
                    yield right
        root = self.root() if p is None else p
        for position in _inorder(root):
            yield position

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
    from random import randrange
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

if __name__ == "__main__":
    test_case_bfs_tree()
    test_case_bst()
