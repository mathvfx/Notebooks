//
//  NearestNeighbor.hpp
//  KNearestNeighbor
//
//  Created by Alex on 4/24/20.
//  Copyright © 2020 Alex Lim. All rights reserved.
//

#ifndef KNearestNeighbor_NearestNeighbor_hpp
#define KNearestNeighbor_NearestNeighbor_hpp

#include <algorithm>
#include <array>
#include <limits>
#include <vector>

#include "Globals.hpp"
#include "BoundedVector.hpp"
#include "CompleteBinaryTree.hpp"
#include "WavefrontObject.hpp"

namespace KNN {

    class NearestNeighbor : public CompleteBinaryTree {
    public:
        NearestNeighbor() {};
        NearestNeighbor(const WavefrontObject&);
//        NearestNeighbor(const std::array<MathVector, DIMENSION>&);
//        NearestNeighbor(const std::vector<MathVector>&);
//        NearestNeighbor(const std::vector<CBT_POD>&);

        void search(CBT_POD& output, const MathVector& query);

        void ksearch(
                std::vector<CBT_POD>& output,
                const MathVector& query,
                size_t k=3
                );

    private:
        void build_static_kdtree(
                std::vector<CBT_POD>& ptr_list,
                size_t start_depth = 0
                );
        
        // Convenient function to cycle coordinate axis, sort on axis, and
        // return median node.
        // RETURN: Node index to represent location in binary tree
        size_t _axis_sort_median(
                std::vector<CBT_POD>::iterator itr_begin,
                std::vector<CBT_POD>::iterator itr_end,
                size_t depth
                );
        
        // Helper function to recursively add nodes to k-d tree
        // (a specialized binary search tree data structure)
        void _kdtree(
                std::vector<CBT_POD>::iterator itr_begin,
                std::vector<CBT_POD>::iterator itr_end,
                size_t depth = 0,
                size_t node_idx = 0
                );
        

        // Helper function to recursively search for k closest point for k > 0.
        void _visit_k_subtree(  // EXPERIMENT!
                const MathVector& query,
                BoundedVector& output,
                const size_t node_idx = 0, // begin with root node
                const size_t depth = 0
                );
    }; // END class NearestNeighbor

} // END namespace KNN

#endif /* KNearestNeighbor_NearestNeighbor_hpp */
