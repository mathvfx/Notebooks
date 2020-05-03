//
//  main.cpp
//  kNearestNeighbor
//
//  Created by Alex on 5/1/20.
//  Copyright © 2020 Alex Lim. All rights reserved.
//

#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

#include <boost/program_options.hpp>

#include "Globals.hpp"
#include "NearestNeighbor.hpp"
#include "Vector.hpp"
#include "WavefrontObject.hpp"



int main(int argc, const char * argv[]) {
    namespace BPO = boost::program_options;
    bool is_help {};
    size_t k_value {};
    std::string file_path {};


    // Setting up program options
    
    BPO::options_description desc(
        ">>> knnsearch [options] query_1 ... query_n\n\n"
        "Allowable Options");
    desc.add_options()
        ("help,h", BPO::bool_switch(&is_help),
            "Display this help narrative.")
        ("k,k", BPO::value<size_t>(&k_value)->default_value(1),
            "Specify how many nearest points to search.")
        ("query,q", BPO::value<std::vector<KNN::PRECISION>>(),
            "Specify query vector (test point) to search the point cloud.")
        ("objfile", BPO::value<std::string>(&file_path),
            "Specify path of Wavefront OBJ file.")
        ;

    BPO::positional_options_description positional;
    positional.add("query", -1);

    BPO::command_line_parser CLI_parser {argc, argv};
    CLI_parser.options(desc);
    CLI_parser.positional(positional);
    
    
    // Process program options
    
    BPO::variables_map vm;
    try {
        auto parsed_result = CLI_parser.run();
        BPO::store(parsed_result, vm);
        BPO::notify(vm);
    } catch (const std::exception& e) {
        std::cerr << e.what() << "\n";
        return -1;
    }
    
    
    // Check resulting conditions and variables of processed program options
    
    if (is_help) {
        KNN::ProgramHeader();
        std::cout <<
        "knnsearch will search for some k nearest points within a 3D point cloud using\n"
        "given query vector. Only quantative-valued point cloud (training data) and\n"
        "query vectors (test set) are supported.\n\n"
        "Currently, only Wavefront OBJ file format are supported for training sets.\n\n"
        "Example usage:\n"
        "   knnsearch --objfile ./point_cloud.obj -k 7 -q 0 0 0\n\n"
            << desc << "\n\n";
        return 0;
    }
    
    if (vm["objfile"].empty()) {
        KNN::ProgramHeader();
        std::cerr << "You must provide a proper point cloud file."
                  << std::endl;
        return -1;
    }
        
    if (vm["query"].empty()) {
        KNN::ProgramHeader();
        std::cerr << "You must specify a query with proper dimension."
                  << std::endl;
        return -1;
    }
    
    auto query = vm["query"].as<std::vector<KNN::PRECISION>>();
    if (query.size() != KNN::DIMENSION)
        query.resize(KNN::DIMENSION);
        
    const KNN::MathVector test_point {query[0], query[1], query[2]};
    
    KNN::ProgramHeader();
    KNN::WavefrontObject wavefront_file {file_path};
    KNN::NearestNeighbor point_cloud {wavefront_file};
    std::vector<KNN::CBT_POD> result;
    point_cloud.ksearch(result, test_point, k_value);
    
    std::cout << "\t" << k_value << "-nearest points found (in ascending order):\n";
    for (size_t i {}; i < k_value; ++i)
        std::cout << "\t\t[" << result[i].ptnum << "]  at  "
                  << std::setprecision(8) << *result[i].ptcoord << "\n";
    std::cout << std::endl;
    
    return 0;
}
