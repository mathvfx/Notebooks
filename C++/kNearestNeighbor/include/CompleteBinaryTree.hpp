//
//  CompleteBinaryTree.hpp
//  KNearestNeighbor
//
//  Created by Alex on 4/20/20.
//  Copyright © 2020 Alex Lim. All rights reserved.
//

#ifndef KNearestNeighbor_CompleteBinaryTree_hpp
#define KNearestNeighbor_CompleteBinaryTree_hpp

#include <cmath> // floor, log2
#include <queue>
#include <vector>

#include "Globals.hpp"
#include "Vector.hpp"

namespace KNN {
    
    // Type-alias
    using MathVector = MATH::Vector<DIMENSION, PRECISION>;
    
    // Extensible plain-old-data container
    struct CBT_POD {
        MathVector* ptcoord {}; // pointer to a point coordinate
        size_t ptnum {}; // corresponding point number
    };

    /*
        CompleteBinaryTree (CBT) is implemented as a full and complete binary
        tree data structure using heap array as its underlying data storage.
        Methods are implemented to mimic node-based tree operation. CBT class
        may be efficient if binary tree is balanced and mostly full. Otherwise,
        using a generalized, actual node-based binary tree data structures may
        be preferred.
     */
    class CompleteBinaryTree {
    public:
        CompleteBinaryTree() {}; // default CTOR
        CompleteBinaryTree(const size_t max_number_of_nodes);
        CompleteBinaryTree(const CompleteBinaryTree&); // Copy-CTOR
        CompleteBinaryTree(CompleteBinaryTree&&) noexcept; //Move-CTOR
        CompleteBinaryTree& operator= (const CompleteBinaryTree&); //Copy-Assgn
        CompleteBinaryTree& operator= (CompleteBinaryTree&&) noexcept; //Move-Assgn
        virtual ~CompleteBinaryTree() = default;
        
        // Accessors
        const CBT_POD& root(const size_t node_idx = 0) const;
        const CBT_POD& parent(const size_t node_idx) const;
        const CBT_POD& left_child(const size_t node_idx) const;
        const CBT_POD& right_child(const size_t node_idx) const;
        bool has_node(const size_t node_idx=0) const;
        bool has_left_child(const size_t node_idx) const;
        bool has_right_child(const size_t node_idx) const;
        size_t left_child_idx(const size_t node_idx) const;
        size_t right_child_idx(const size_t node_idx) const;
        
        size_t height(const size_t node_idx) const;
        bool is_empty() const { return num_nodes == 0; }
        size_t size() const { return num_nodes; }

        // Mutators
        // All return for add_* methods are corresponding binary tree node index
        size_t add_node(CBT_POD&, const size_t node_idx);
        size_t add_node(CBT_POD&&, const size_t node_idx);
        size_t add_root(CBT_POD&);
        size_t add_root(CBT_POD&&);
        size_t add_left_child(CBT_POD&, const size_t node_idx);
        size_t add_left_child(CBT_POD&&, const size_t node_idx);
        size_t add_right_child(CBT_POD&, const size_t node_idx);
        size_t add_right_child(CBT_POD&&, const size_t node_idx);

        void build_breath_first(const std::vector<MathVector>&);
//        void traverse_breadth_first() const;

        CBT_POD& operator[] (size_t idx);
        const CBT_POD& operator[] (size_t idx) const;

    protected:
        size_t reserved_capacity {};
        std::vector<CBT_POD> cbt_pod_list;

    private:
        size_t num_nodes {};
    };

} // END namespace KNN
#endif /* KNearestNeighbor_CompleteBinaryTree_hpp */
