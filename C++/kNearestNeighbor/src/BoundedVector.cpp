//
//  BoundedVector.cpp
//  KNearestNeighbor
//
//  Created by Alex on 4/28/20.
//  Copyright © 2020 Alex Lim. All rights reserved.
//

#include "BoundedVector.hpp"

KNN::BoundedVector::BoundedVector(size_t k)
: k_number{k} {
    sorted_pair.reserve(k+1); // Additional element for pre-boundary truncates
}


void KNN::BoundedVector::push(CBT_POD elem, PRECISION dist) {
    sorted_pair.push_back({elem, dist});
    
    using PAIR = std::pair<CBT_POD, PRECISION>;
    std::sort(
        sorted_pair.begin(),
        sorted_pair.end(),
        [](const PAIR& a, const PAIR& b){ return a.second < b.second; }
        );
        
    if (sorted_pair.size() > k_number)
        sorted_pair.pop_back();
}


const KNN::CBT_POD& KNN::BoundedVector::operator[] (size_t idx) const {
    return sorted_pair.at(idx).first;
}
