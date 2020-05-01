//
//  WavefrontObject.cpp
//  KNearestNeighbor
//
//  Created by Alex on 4/14/20.
//  Copyright © 2020 Alex Lim. All rights reserved.
//

#include "WavefrontObject.hpp"

KNN::WavefrontObject::WavefrontObject()
    : point_list{}
    , _file_loaded_state{false}
    , obj_path{} {

}


KNN::WavefrontObject::WavefrontObject(std::string_view file_path) {
    obj_path = KNN::VerifyMyFilePath(file_path.data());
    _file_loaded_state = load_obj_file(obj_path.c_str());
}


bool KNN::WavefrontObject::load_obj_file(std::string_view file_path) {
    std::ifstream obj_file {KNN::OpenFile(file_path.data())};
    if (obj_file.good()) {
        _file_loaded_state = true;
        MATH::Vector<DIMENSION, PRECISION> point; // Assuming .obj uses 3D-point
        std::array<PRECISION, DIMENSION> stored_min {};
        std::array<PRECISION, DIMENSION> stored_max {};
        std::string line;
        line.reserve(128);
        
        std::regex re_houdini_pt {R"(^\s*#\s(\d+)\spoints.*)",
                                    std::regex_constants::icase};
        std::smatch ptcount;

        std::string keyword;
        while(std::getline(obj_file, line)) { //TODO: optimize by block-read?
            std::istringstream ss {std::move(line)};
            ss >> keyword;
            if (keyword == "v") {
                for (size_t i{}; i < DIMENSION; ++i) {
                    ss >> point[i];
                    if (stored_min[i] >= point[i]) stored_min[i] = point[i];
                    if (stored_max[i] <= point[i]) stored_max[i] = point[i];
                }
                point_list.push_back(std::move(point));
                continue;
            }
            if (keyword == "#") {
                if (std::regex_match(line, ptcount, re_houdini_pt))
                    // This is specific to .obj output from Houdini
                    point_list.reserve(std::stoull(ptcount[1].str()));
                continue;
            }
            if (keyword == "g")
                continue;
            break; // Completed vertex extraction; don't process further.
        }
        obj_file.close();
        min_bound = stored_min;
        max_bound = stored_max;
        return true;
    }
    return false;
}
