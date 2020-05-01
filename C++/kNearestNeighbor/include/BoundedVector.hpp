//
//  BoundedPriorityQueue.hpp
//  KNearestNeighbor
//
//  Created by Alex on 4/28/20.
//  Copyright © 2020 Alex Lim. All rights reserved.
//

#ifndef KNearestNeighbor_BoundedVector_hpp
#define KNearestNeighbor_BoundedVector_hpp

#include <algorithm>
#include <utility>
#include <vector>

#include "CompleteBinaryTree.hpp"

namespace KNN {
    
    /*
        Instead of writing a wrapper around a Priority Queue, we wrap around a
        simple std::vector as a Bounded Vector. As each element is pushed into
        std::vector, we immediately sort them. Therefore, at every push(),
        existing elements are in a mostly-sorted state. This approach allows us
        to access vector components at random while keeping only k-best items.
        
        BoundedVector is specific to NearestNeighbor code.
    */
    class BoundedVector {
    public:
        BoundedVector() = delete;
        BoundedVector(size_t k);

        void push(CBT_POD elem, PRECISION);
    
        bool empty() {
            return size() == 0;
        }
        
        size_t max_bound() {
            return k_number;
        }
        
        PRECISION priority(size_t idx) {
            return sorted_pair.at(idx).second;
        }
        
        size_t size() {
            return sorted_pair.size();
        }
        
        // Operator overload
        const CBT_POD& operator[] (size_t idx) const;

    private:
        size_t k_number;
        std::vector<std::pair<CBT_POD, PRECISION>> sorted_pair;

    }; // END class BoundedPriorityQueue
} // END namespace KNN

#endif /* KNearestNeighbor_BoundedVector_hpp */
