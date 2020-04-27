#ifndef KNearestNeighbor_WavefrontObject_hpp
#define KNearestNeighbor_WavefrontObject_hpp

#include <array>
#include <filesystem>
#include <fstream>
#include <regex>
#include <sstream>
#include <string>
#include <vector>

#include "Globals.hpp"
#include "Vector.hpp"

namespace KNN {

    class WavefrontObject {
    public:
        WavefrontObject();
        WavefrontObject(std::string_view file_path);

        bool load_obj_file(std::string_view file_path);
//        void write_point_obj_file(std::string_view file_path); // TODO:

        bool is_empty() const {
            return point_list.size() == 0;
        }
        bool is_loaded() const {
            return _file_loaded_state;
        }
        MATH::Vector<DIMENSION> get_max_bound() const {
            return max_bound;
        }
        MATH::Vector<DIMENSION> get_min_bound() const {
            return min_bound;
        }
        size_t get_point_count() const {
            return point_list.size();
        }
        const MATH::Vector<DIMENSION>& operator[] (size_t ptnum) const {
            return point_list.at(ptnum);
        }
        
    private:
        MATH::Vector<DIMENSION> min_bound {};
        MATH::Vector<DIMENSION> max_bound {};
        std::vector<MATH::Vector<DIMENSION, PRECISION>> point_list;
        
        bool _file_loaded_state; // Track file loading state
        std::filesystem::path obj_path;

    }; // END class WavefrontObject
} // END namespace KNN

#endif /* KNearestNeighbor_WavefrontObject_hpp */
