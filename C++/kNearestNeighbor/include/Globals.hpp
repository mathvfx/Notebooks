//
//  Globals.hpp
//  KNearestNeighbor
//
//  Copyright © 2020 Alex Lim. All rights reserved.
//

#ifndef KNearestNeighbor_Globals_hpp
#define KNearestNeighbor_Globals_hpp

#include <filesystem>
#include <fstream>
#include <iostream>
#include <limits>
#include <string>
#include <type_traits>

namespace KNN {

// Default numeric-type precision. Expect numeric type.
using PRECISION = double;


// Dimension of Math Vector we're operating with.
constexpr static size_t DIMENSION = 3;


// Verify file path string is a valid filesystem path.
// RETURN: empty path if invalid file path.
std::filesystem::path VerifyMyFilePath(const std::string& my_path);


// Factory function to handle file-opening failures with exceptions
// RETURN: an opened file stream object or raise exceptions
std::ifstream OpenFile(
            const std::string& my_path,
            std::ios_base::openmode mode = std::ios_base::in
            );


// Floating-point value equality comparison.
// RETURN: true if floating-points are equal within epsilon tolerance.
template <typename T>
constexpr bool FpEquality(
                const T& x,
                const T& y,
                T epsilon=std::numeric_limits<T>::epsilon()) {
    if (std::is_floating_point<T>())
        return (x <= (y + epsilon)) && (x >= (y - epsilon));
    return (x == y);
    /*
     The idea for FpEquality is as follow:
     Suppose x is any real number, and epsilon is any small, but nonnegative
     real number. Then we have x - epsilon <= x <= x + epsilon. We can thus say
     y1 <= x <= y2, where y1 = x - epsilon and y2 = x + epsilon.
     Now, as the limit of epsilon approaches 0, it follows that x = y1
     and x = y2, and therefore y1 = y2 = y imply x = y as desired.
    */
}


}; // END namespace KNN

#endif /* KNearestNeighbor_Globals_hpp */
