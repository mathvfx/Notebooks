//
//  NearestNeighbor.cpp
//  KNearestNeighbor
//
//  Created by Alex on 4/24/20.
//  Copyright © 2020 Alex Lim. All rights reserved.
//

#include "NearestNeighbor.hpp"

KNN::NearestNeighbor::NearestNeighbor(const WavefrontObject& pt_obj)
: CompleteBinaryTree{pt_obj.get_point_count()} {
    if (pt_obj.is_loaded() and !pt_obj.is_empty()) {
    
        // Construct first temporary ptr list pointing to wavefront point list.
        std::vector<CBT_POD> ptr_list;
        ptr_list.resize(pt_obj.get_point_count(), CBT_POD());
        for (size_t i{}; i < pt_obj.get_point_count(); ++i)
             ptr_list[i] = {const_cast<MathVector* const>(&pt_obj[i]), i};

        // Then build a median-of-medians kd-tree using temporary pointer list
        build_static_kdtree(ptr_list);

        // Manual checking....
        
        for(const auto& i: cbt_pod_list)
            if ( i.ptcoord )
                std::cout << "  [" << i.ptnum << "]:  " << *i.ptcoord << std::endl;
            else
                std::cout << "  [?]" << std::endl;
        
    }
}

void KNN::NearestNeighbor::search( const MathVector& query, CBT_POD& result) {
// TODO: Handle equal points.
//       Currently we are assuming every points are unique (no points equal).
//       We will need a way to handle duplicate points.
    if(!is_empty()) {
        MathVector query_pt {query};
        
        // Use root node as a starting condition
        auto node = root();
        auto nearest_node = const_cast<CBT_POD*>(&node);
        auto min_dist = query.distance(*(*nearest_node).ptcoord);

        size_t node_idx = 0; // begin with root node
        PRECISION left_dist = std::numeric_limits<PRECISION>::max();
        PRECISION right_dist = std::numeric_limits<PRECISION>::max();
        
        while (has_node(node_idx)) {
            // Check left node
            if (has_left_child(node_idx))
                left_dist = query.distance(*left_child(node_idx).ptcoord);
            else if (!has_right_child(node_idx))
                break; // Break if no left and right child
                
            if (has_right_child(node_idx))
                right_dist = query.distance(*right_child(node_idx).ptcoord);
            else {
                if (left_dist < min_dist) {
                    min_dist = left_dist;
                    nearest_node = const_cast<CBT_POD*>(&left_child(node_idx));
                }
                node_idx = left_child_idx(node_idx); // advance to left branch
                continue;

            }
            
            if (left_dist < right_dist) {
                if (left_dist < min_dist) {
                    min_dist = left_dist;
                    nearest_node = const_cast<CBT_POD*>(&left_child(node_idx));
                }
                node_idx = left_child_idx(node_idx); // advance to left branch
                continue;
            }
            if (right_dist < min_dist) {
                min_dist = right_dist;
                nearest_node = const_cast<CBT_POD*>(&right_child(node_idx));
            }
            node_idx = right_child_idx(node_idx); // advance to right branch
        }
//        std::cout << " [" << (*nearest_node).ptnum << "]:  " << *(*nearest_node).ptcoord << std::endl;
        result = *nearest_node;
    }
}



// Private helper functions


void KNN::NearestNeighbor::build_static_kdtree( std::vector<CBT_POD>& ptr_list,
                                                size_t start_depth ) {
    if (ptr_list.size() > 0) {
        auto itr_begin = ptr_list.begin();
        auto itr_end = ptr_list.end();
        
        // Set root node first
        size_t median = _axis_sort_median(itr_begin, itr_end, start_depth);
        size_t curr_node = add_root(std::move(*(itr_begin + median)));
        
        // Recursively split to left subtree
        _kdtree(itr_begin, itr_begin + median, start_depth+1, curr_node);
        
        // Recursively split to right subtree
        _kdtree(itr_begin + median+1, itr_end, start_depth+1, curr_node);
    }
}

void KNN::NearestNeighbor::_kdtree( std::vector<CBT_POD>::iterator itr_begin,
                                    std::vector<CBT_POD>::iterator itr_end,
                                    size_t depth,
                                    size_t node_idx ) {
    // Base Case
    if (std::distance(itr_begin, itr_end) == 1)
        if (!has_left_child(node_idx))
            add_left_child(std::move(*itr_begin), node_idx);
        else
            add_right_child(std::move(*itr_begin), node_idx);
            
    // Recursive case
    else if (itr_begin < itr_end) {
        size_t median = _axis_sort_median(itr_begin, itr_end, depth);

        // Adding to left child
        size_t curr_idx {};
        if (!has_left_child(node_idx))
            curr_idx = add_left_child(std::move(*(itr_begin+median)), node_idx);
        else
            curr_idx = add_right_child(std::move(*(itr_begin+median)), node_idx);
        _kdtree(itr_begin, itr_begin+median, depth+1, curr_idx);
        
        // Adding to right child -- only if we still have items to process
        if (itr_begin+median+1 < itr_end)
            _kdtree(itr_begin+median+1, itr_end, depth+1, curr_idx);
    }
}

size_t KNN::NearestNeighbor::_axis_sort_median(
                                std::vector<CBT_POD>::iterator itr_begin,
                                std::vector<CBT_POD>::iterator itr_end,
                                size_t depth) {
    size_t axis = depth % DIMENSION;
    std::sort(
            itr_begin,
            itr_end,
            [&axis](const CBT_POD& a, const CBT_POD& b) -> bool
                {return (*a.ptcoord)[axis] < (*b.ptcoord)[axis];} );
    return std::distance(itr_begin, itr_end) / 2; // flooring by truncation
}
