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
#include <stdexcept>
#include <vector>

#include "Globals.hpp"
#include "CompleteBinaryTree.hpp"
#include "WavefrontObject.hpp"

namespace KNN {

    class NearestNeighbor : public CompleteBinaryTree {
    public:
        NearestNeighbor() = delete; // Empty CTOR shouldn't be allowed here
        NearestNeighbor(const WavefrontObject&);
//        NearestNeighbor(const std::array<MathVector, DIMENSION>&);
//        NearestNeighbor(const std::vector<MathVector>&);
//        NearestNeighbor(const std::vector<CBT_POD>&);

        void search(const MathVector& query, CBT_POD& result);

    private:
        void build_static_kdtree( std::vector<CBT_POD>& ptr_list,
                                    size_t start_depth = 0);
        
        size_t _axis_sort_median( std::vector<CBT_POD>::iterator itr_begin,
                                    std::vector<CBT_POD>::iterator itr_end,
                                    size_t depth );
                        
        void _kdtree( std::vector<CBT_POD>::iterator itr_begin,
                        std::vector<CBT_POD>::iterator itr_end,
                        size_t depth = 0,
                        size_t node_idx = 0  );
    }; // END class NearestNeighbor

} // END namespace KNN

#endif /* KNearestNeighbor_NearestNeighbor_hpp */
