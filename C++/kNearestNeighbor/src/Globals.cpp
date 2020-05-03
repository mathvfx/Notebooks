//
//  Globals.cpp
//  KNearestNeighbor
//
//  Created by Alex on 4/14/20.
//  Copyright © 2020 Alex Lim. All rights reserved.
//

#include "Globals.hpp"


 void KNN::ProgramHeader() {
    std::cout <<
    "\n"
    "\tk-Nearest Neighbor Search\n"
    "\t< Alex Lim  https://mathvfx.github.io  v2020.05.02 >\n"
        << std::endl;
}


std::filesystem::path KNN::VerifyMyFilePath(const std::string& my_path) {
    namespace FS = std::filesystem;
    FS::path file_path {my_path};
    file_path.make_preferred();
    if (!FS::exists(file_path))
        throw std::ios_base::failure {"[File Not Exist]: " + my_path};
    if (!FS::is_regular_file(file_path))
        throw std::ios_base::failure {"[Not a File]: " + my_path};
    return FS::canonical(file_path);
}


std::ifstream KNN::OpenFile(const std::string& my_path,
                            std::ios_base::openmode mode) {
    std::ifstream my_file {my_path, mode};
    if (!my_file.is_open())
        throw std::runtime_error {"[Cannot Open File]: " + my_path};
    my_file.exceptions(std::ifstream::badbit);
    return my_file;
}
