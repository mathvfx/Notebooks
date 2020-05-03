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
    }
}


void KNN::NearestNeighbor::search(CBT_POD& output, const MathVector& query) {
    if(!is_empty())
        _visit_single_subtree(query, output);
}


void KNN::NearestNeighbor::ksearch(
                                    std::vector<CBT_POD>& output,
                                    const MathVector& query,
                                    size_t k ) {
    if (!is_empty()) {
        if (k > 1) {
            if (k > size()) k = size(); // Ensure k is clamped at size of data
            BoundedVector k_best {k};
            _visit_k_subtree(query, k_best);
            output.clear();
            output.resize(k);
            for (size_t i {}; i < k; ++i)
                output[i] = k_best[i];
        } else {
            CBT_POD best;
            _visit_single_subtree(query, best);
            output.clear();
            output.push_back(best);
        }
    } // outer if
}


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
    return std::distance(itr_begin, itr_end) / 2; // floor by truncation
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


void KNN::NearestNeighbor::_visit_single_subtree(
                                const MathVector& query,
                                CBT_POD& output,
                                const size_t node_idx,
                                const size_t depth,
                                PRECISION best_dist ) {
    if (has_node(node_idx)) {
        auto axis = depth % DIMENSION;
        auto curr_node = root(node_idx);
        auto dist = query.distance(*curr_node.ptcoord);
        
        if (dist < best_dist) {
            best_dist = dist;
            output = curr_node;
        }
        
        if (query[axis] < (*curr_node.ptcoord)[axis])
            _visit_single_subtree( query,
                                    output,
                                    left_child_idx(node_idx),
                                    depth+1,
                                    best_dist
                                    );
        else
            _visit_single_subtree( query,
                                    output,
                                    right_child_idx(node_idx),
                                    depth+1,
                                    best_dist
                                    );
    }
}


void KNN::NearestNeighbor::_visit_k_subtree(
                                const MathVector& query,
                                BoundedVector& output,
                                const size_t node_idx,
                                const size_t depth ) {
    if (has_node(node_idx)) {
        auto axis = depth % DIMENSION;
        auto curr_ptcoord = *root(node_idx).ptcoord;
        auto dist = query.distance(curr_ptcoord);
        output.push(root(node_idx), dist);

        if (query[axis] < (curr_ptcoord)[axis]) {
            _visit_k_subtree(query, output, left_child_idx(node_idx), depth+1);
            if (output.size() < output.max_bound()
                    or std::abs(curr_ptcoord[axis] - query[axis]) < output.priority(output.size()-1))
                _visit_k_subtree(query, output, right_child_idx(node_idx), depth+1);
        } else {
            _visit_k_subtree(query, output, right_child_idx(node_idx), depth+1);
            if (output.size() < output.max_bound()
                    or std::abs(curr_ptcoord[axis] - query[axis]) < output.priority(output.size()-1))
                _visit_k_subtree(query, output, left_child_idx(node_idx), depth+1);
        }
    }
}
