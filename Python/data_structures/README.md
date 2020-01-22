# Notebook
This notebook serves as my public repository of various learning notes and exercises spanning Mathematics, programming, Houdini tools, and others. I make effort toward producing quality and accurate notes and, therefore, my content output may be slow. But contents here will be updated and accumulated over time. 


### Data Structures
While data structures here are quite elementary and common, still they form a foundation in solving data problems pertaining to in storage and retrieval efficiencies. We begin with a very specialized data structures such as stack and queues, linked-list, and binary trees. From binary trees, we begin to generalize toward well-known m-ary tree and graphs. Having these back-bone and programming trainings, these will help us see problem-solution structures and consider their applications.


### Learning Outcome: Data Structures
 1. **_Stack and Queue and Deque_**
    * Understand an object-oriented design method called Abstract Base Class (ABC); how ABC can guarantee that such object will have certain method available in a larger software context; also useful as a "checklist" of what needs to be implemented in an Abstract Data Type (ADT).
    * Understand design and encapsulation differences between Stack, Queue, and Double-Ended Queue.
    * Possible applications of Queue could be to build and traverse level-order binary tree; using Deque to implement _round-robin games_ and _modeling ticket booth_, etc.

 1. **_Linked-List_**
    * Understand differences between array and linked-list; pros and cons in terms of memory usage and random access time.
    * Understand the differences between singly, circular, and doubly linked-list.
    * Understand the challenges in terms of their implementations and ease of use.

 1. _**Binary Tree** (special case of m-ary tree&mdash; which also special case of Graph)_
    * Understand property of binary tree; how to build and traverse a tree; relations between BFS and Queue, DFS and Stack.
    * Know the names and types of trees and their mathematical properties.
    * Possible applications may include: _binary space partitioning_, _kd tree_, _nearest-neighbor issue_, _heap_ and _priority queue_, etc.

 1. **_Priority Queue_**
    * Understand multiple inheritance by using previously implemented ADTs in OOP fashion.
    * Understand issues pertaining to method resolution order (MRO)in terms of how Python determine which method to use in its inheritance tree.
    * Understand binary heaps, and how we can exploit properties of binary heaps to better utilize resources (array instead of linked-list in this case)
    * Aware that implementation of _Heapsort_ can be viewed as a special case of Priority Queue implementation (without the _Item_ object)

 1. **_Maps and Sets_**
    * Using similar methods of Priority Queue, we attempt to implement list maps using "key" as our access indices. But using such list maps are largely a O(n)-time complexity unless we also utilize binary search to pre-sort our data.
    * Understant concepts of Python's Dictionary (a.k.a. associative array) and hashing functions. 
    * Understand the concept of hashing function as an intermediary to generate proper array indices in order for regular list/array access.
    * Understand the broader issue associated with hash collision, and basic collision resolution methods, and the reasons behind such collisions, and broader consequences in security.
    * Understand the implementation of Set (_Set Theory_ definition) is really just a special case implementation of Maps (without _Item_ object storage). Note that _key_ in a traditional Map must be unique, thus we can exploit this feature for Set.
    * Aware that Multimaps and Multisets are also special case implementation of Maps and Sets.
      * Multiset: keys are now allowed to be duplicates using container.
      * Multimap: Same keys can now be mapped to multiple values.
    * Possible application of Maps and Sets may include:  _finding extrema in a subset_, _Skip List_


### To-Do's
 1. Common sort algorithms
 1. Basic graphs algorithms
