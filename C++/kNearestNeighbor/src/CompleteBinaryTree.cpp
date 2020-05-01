//
//  CompleteBinaryTree.cpp
//  KNearestNeighbor
//
//  Created by Alex on 4/20/20.
//  Copyright © 2020 Alex Lim. All rights reserved.
//

#include "CompleteBinaryTree.hpp"

// Rule of Big Five

KNN::CompleteBinaryTree::CompleteBinaryTree(const size_t max_number_of_nodes) {
    // reserved_capacity is node capacity for complete and full BinTree
    reserved_capacity = std::pow(2, height(max_number_of_nodes)+1) - 1;
    cbt_pod_list.resize(reserved_capacity, CBT_POD());
}


KNN::CompleteBinaryTree::CompleteBinaryTree(const CompleteBinaryTree& other)
: reserved_capacity{other.reserved_capacity}
, num_nodes{other.num_nodes} {
    cbt_pod_list.reserve(reserved_capacity);
    for (const auto& i : other.cbt_pod_list) // TODO: check case other.num_nodes vs capacity
        cbt_pod_list.push_back(i);
}


KNN::CompleteBinaryTree::CompleteBinaryTree(CompleteBinaryTree&& other) noexcept
: reserved_capacity{other.reserved_capacity}
, num_nodes {other.num_nodes} {
    cbt_pod_list.reserve(reserved_capacity);
    cbt_pod_list = other.cbt_pod_list; // copying addresses only
    other.cbt_pod_list.clear();
    other.reserved_capacity = 0;
    other.num_nodes = 0;
}


KNN::CompleteBinaryTree& KNN::CompleteBinaryTree::operator= (
                                            const CompleteBinaryTree& other) {
    if (this == &other) return *this;
    reserved_capacity = other.reserved_capacity;
    num_nodes = other.num_nodes;
    cbt_pod_list.clear();
    cbt_pod_list.reserve(reserved_capacity);
    for (const auto& i: other.cbt_pod_list)
        cbt_pod_list.push_back(i);
    return *this;
}


KNN::CompleteBinaryTree& KNN::CompleteBinaryTree::operator= (
                                        CompleteBinaryTree&& other) noexcept {
    if (this == &other) return *this;
    cbt_pod_list.clear();
    reserved_capacity = other.reserved_capacity;
    num_nodes = other.num_nodes;
    cbt_pod_list.reserve(reserved_capacity);
    cbt_pod_list = other.cbt_pod_list; // copying addresses only
    other.cbt_pod_list.clear();
    other.num_nodes = 0;
    other.reserved_capacity = 0;
    return *this;
}


// General class methods


size_t KNN::CompleteBinaryTree::height(const size_t node_idx) const {
    return std::floor(std::log2(node_idx+1));
}


const KNN::CBT_POD& KNN::CompleteBinaryTree::root(const size_t node_idx) const {
    return cbt_pod_list[node_idx];
}


const KNN::CBT_POD& KNN::CompleteBinaryTree::parent(const size_t node_idx) const {
    size_t idx = node_idx > 0 ? (node_idx - 1)/2 : 0;
        // Using integer division truncation to act as flooring there.
    return cbt_pod_list[idx];
}


const KNN::CBT_POD& KNN::CompleteBinaryTree::left_child(const size_t node_idx) const {
    const size_t idx = 2*node_idx + 1;
    if ( idx >= reserved_capacity or !cbt_pod_list[idx].ptcoord)
        throw std::out_of_range {"No left-child node exist."};
    return cbt_pod_list[idx];
}


const KNN::CBT_POD& KNN::CompleteBinaryTree::right_child(const size_t node_idx) const  {
    const size_t idx = 2*node_idx + 2;
    if (idx >= reserved_capacity or !cbt_pod_list[idx].ptcoord)
        throw std::out_of_range {"No right-child node exist."};
    return cbt_pod_list[idx];
}


bool KNN::CompleteBinaryTree::has_node(const size_t node_idx) const {
    return static_cast<bool>(cbt_pod_list[node_idx].ptcoord) and node_idx < reserved_capacity;
}


bool KNN::CompleteBinaryTree::has_left_child(const size_t node_idx) const {
    const size_t idx = 2*node_idx + 1;
    return idx < reserved_capacity && cbt_pod_list[idx].ptcoord;
        // As a design patch, we use .ptcoord there to test for nullptr because
        // this turned out to be a level-order tree where last level may
        // potentially contain empty leaf node.
}


bool KNN::CompleteBinaryTree::has_right_child(const size_t node_idx) const {
    const size_t idx = 2*node_idx + 2;
    return idx < reserved_capacity && cbt_pod_list[idx].ptcoord;
        // As a design patch, we use .ptcoord there to test for nullptr because
        // this turned out to be a level-order tree where last level may
        // potentially contain empty leaf node.}
}


size_t KNN::CompleteBinaryTree::left_child_idx(const size_t node_idx) const {
    return 2*node_idx + 1;
}


size_t KNN::CompleteBinaryTree::right_child_idx(const size_t node_idx) const {
    return 2*node_idx + 2;
}


size_t KNN::CompleteBinaryTree::add_node( CBT_POD& pod_data,
                                            const size_t node_idx) {
    if (cbt_pod_list[node_idx].ptcoord != nullptr)
        throw std::out_of_range {"Root node is not empty."};
    cbt_pod_list[node_idx] = pod_data;
    ++num_nodes;
    return node_idx; // 0 is the index of root node
}


size_t KNN::CompleteBinaryTree::add_node( CBT_POD&& pod_data,
                                            const size_t node_idx) {
    if (cbt_pod_list[node_idx].ptcoord != nullptr)
        throw std::out_of_range {"Root node is not empty."};
    cbt_pod_list[node_idx] = std::move(pod_data);
    ++num_nodes;
    return node_idx;
}


size_t KNN::CompleteBinaryTree::add_root(CBT_POD& pod_data) {
    return add_node(pod_data, 0); // 0 is the index of root node
}


size_t KNN::CompleteBinaryTree::add_root(CBT_POD&& pod_data) {
    return add_node(std::move(pod_data), 0);
}


size_t KNN::CompleteBinaryTree::add_left_child( CBT_POD& pod_data,
                                                const size_t node_idx) {
    if (has_left_child(node_idx))
        throw std::out_of_range {"Left-child node is not empty."};
    size_t left_node_idx = 2*node_idx + 1;
    cbt_pod_list[left_node_idx] = pod_data;
    ++num_nodes;
    return left_node_idx;
}


size_t KNN::CompleteBinaryTree::add_left_child( CBT_POD&& pod_data,
                                                const size_t node_idx) {
    if (has_left_child(node_idx))
        throw std::out_of_range {"Left-child node is not empty."};
    size_t left_node_idx = 2*node_idx + 1;
    cbt_pod_list[left_node_idx] = std::move(pod_data);
    ++num_nodes;
    return left_node_idx;
}


size_t KNN::CompleteBinaryTree::add_right_child( CBT_POD& pod_data,
                                                const size_t node_idx) {
    if (has_right_child(node_idx))
        throw std::out_of_range {"Right-child node is not empty."};
    size_t right_node_idx = 2*node_idx + 2;
    cbt_pod_list[right_node_idx] = pod_data;
    ++num_nodes;
    return right_node_idx;
}


size_t KNN::CompleteBinaryTree::add_right_child( CBT_POD&& pod_data,
                                                const size_t node_idx) {
    if (has_right_child(node_idx))
        throw std::out_of_range {"Right-child node is not empty."};
    size_t right_node_idx = 2*node_idx + 2;
    cbt_pod_list[right_node_idx] = std::move(pod_data);
    ++num_nodes;
    return right_node_idx;
}


void KNN::CompleteBinaryTree::build_breath_first(
                            const std::vector<MathVector>& build_list) {
    auto itr = build_list.begin();
    std::queue<size_t> levels;
    CBT_POD my_pod = {const_cast<MathVector* const>(&*(itr++)), 0};
    levels.push(add_root(std::move(my_pod)));

    size_t node_idx;
    size_t left_idx;
    size_t right_idx;
    for (size_t i{1}; i < reserved_capacity; ++i) {
        node_idx = levels.front();
        levels.pop();
        my_pod = {const_cast<MathVector* const>(&*(itr++)), i};
        left_idx = add_left_child(std::move(my_pod), node_idx);
        if (itr == build_list.end()) break;
        my_pod = {const_cast<MathVector* const>(&*(itr++)), ++i};
        right_idx = add_right_child(std::move(my_pod), node_idx);
        if (itr == build_list.end()) break;
        levels.push(left_idx);
        levels.push(right_idx);
    }
}


const KNN::CBT_POD& KNN::CompleteBinaryTree::operator[] (size_t idx) const {
    return cbt_pod_list.at(idx);
}


KNN::CBT_POD& KNN::CompleteBinaryTree::operator[] (size_t idx) {
    return cbt_pod_list.at(idx);
}
