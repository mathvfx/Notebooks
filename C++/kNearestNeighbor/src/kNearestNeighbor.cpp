//
//  main.cpp
//  kNearestNeighbor
//
//  Created by Alex on 5/1/20.
//  Copyright © 2020 Alex Lim. All rights reserved.
//

#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

#include <boost/algorithm/string/case_conv.hpp>
#include <boost/program_options.hpp>
#include <boost/tokenizer.hpp>

#include "Globals.hpp"
#include "NearestNeighbor.hpp"
#include "Vector.hpp"
#include "WavefrontObject.hpp"

using std::cerr;
using std::cin;
using std::cout;
using std::endl;
using std::flush;
using std::setw;
using std::chrono::high_resolution_clock;

void SimpleCLI(); // Simple command-line interface
void PrintHelp(); // Convenient help-card



int main(int argc, const char * argv[]) {
    KNN::ProgramHeader();
    
    if (argc == 1) {
        SimpleCLI();
        return 0;
    }
    
    // Proceed with program options if CLI is not used
    namespace BPO = boost::program_options;
    bool is_help {};
    size_t k_value {};
    std::string file_path {};


    // Setting up program options
    
    BPO::options_description desc(
        "Program Options:\n"
        "knnsearch [options] query_1 ... query_n\n\n"
        "Allowable Options"
        );
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
        cerr << e.what() << "\n";
        return -1;
    }
        
    // Check resulting conditions and variables of processed program options
    
    if (is_help) {
        PrintHelp();
        cout <<
        "Example usage:\n"
        "   knnsearch --objfile ./point_cloud.obj -k 7 -q 0 0 0\n\n"
            << desc << "\n\n";
        return 0;
    }
    
    if (vm["objfile"].empty()) {
        cerr << "You must provide a proper point cloud file.\n";
        return -1;
    }
        
    if (vm["query"].empty()) {
        cerr << "You must specify a query with proper dimension.\n";
        return -1;
    }
    
    auto query = vm["query"].as<std::vector<KNN::PRECISION>>();
    if (query.size() != KNN::DIMENSION)
        query.resize(KNN::DIMENSION);
        
    const KNN::MathVector test_point {query[0], query[1], query[2]};
    
    // Process commands and display result
    KNN::WavefrontObject wavefront_file {file_path};
    KNN::NearestNeighbor point_cloud {wavefront_file};
    std::vector<KNN::CBT_POD> result;
    point_cloud.ksearch(result, test_point, k_value);
    
    cout << "\t" << k_value << "-nearest points found (in ascending order):\n";
    for (size_t i {}; i < k_value; ++i)
        cout << "\t\tptnum #" << result[i].ptnum << "  at  "
                  << std::setprecision(8) << *result[i].ptcoord << "\n";
    cout << endl;
    
    return 0;
}


void SimpleCLI() {
    std::string cmd;
    size_t kvalue {5};
    KNN::NearestNeighbor ptcloud;
    std::chrono::time_point<high_resolution_clock> t_start;
    std::chrono::time_point<high_resolution_clock> t_end;
    std::chrono::duration<float, std::milli> t_elapse;
    
    while (true) {
        cout << "kNN> " << flush;
        std::getline(cin, cmd);
        if (cin.eof() or cin.bad())
            break;
        
        boost::char_separator<char> delimiter{" "};
        boost::tokenizer<boost::char_separator<char>> cmd_token{cmd, delimiter};
        auto cmd_itr = cmd_token.begin();
        
        // Ignore empty command
        if (cmd_itr == cmd_token.end())
            continue;
        
        // Make cmd keyword lower case for case-insensitive comparison
        auto cmd_keyword = *cmd_itr;
        boost::algorithm::to_lower(cmd_keyword);
        ++cmd_itr;
        
        // Execute commands
        if (cmd_keyword == "query") {
            if (ptcloud.is_empty()) {
                cout << "\t Please load point cloud into memory to proceed.\n"
                     << endl;
                continue;
            }
            if (cmd_itr == cmd_token.end()) {
                cout << "\t Query (proximity) vector value must be specified.\n"
                     << endl;
                continue;
            }
            
            std::vector<KNN::PRECISION> query {};
            while (cmd_itr != cmd_token.end()) {
                query.push_back(std::stold(*cmd_itr));
                ++cmd_itr;
            }
            
            if (query.size() != KNN::DIMENSION)
                query.resize(KNN::DIMENSION);
            
            const KNN::MathVector test_point {query[0], query[1], query[2]};
            std::vector<KNN::CBT_POD> result;
            t_start = high_resolution_clock::now();
            ptcloud.ksearch(result, test_point, kvalue);
            t_end = high_resolution_clock::now();
            cout << "\t" << kvalue << "-nearest points found (in ascending order):\n";
            for (size_t i {}; i < kvalue; ++i)
                cout << "\t\tptnum " << result[i].ptnum << "  at  "
                      << std::setprecision(8) << *result[i].ptcoord << "\n";
            t_elapse = t_end - t_start;
            cout << "\t\t\t\tSearch time elapsed: " << t_elapse.count() << "ms\n";

            cout << endl;
            continue;
            
        } else if (cmd_keyword == "kvalue") {
            if (cmd_itr == cmd_token.end())
                cout << "\t K-value is currently set to " << kvalue << endl;
            else {
                auto old_k = kvalue;
                try {
                    kvalue = std::stoull(cmd_itr->c_str());
                } catch (std::exception) {
                    kvalue = old_k; // ensure default value
                    cout << "\t Invalid argument. Pleast try again." << endl;
                }
            }
            cout << endl;
            continue;
            
        } else if (cmd_keyword == "loadobj") {
            if (cmd_itr == cmd_token.end()) {
                cout << "\t File path not specified..." << endl;
                continue;
            }

            auto obj_path = KNN::VerifyMyFilePath(*cmd_itr);
            cout << "\t Loading Wavefront OBJ file....... " << flush;
            t_start = high_resolution_clock::now();
            KNN::WavefrontObject wavefront {obj_path.c_str()};
            t_end = high_resolution_clock::now();
            t_elapse = t_end - t_start;
            cout << "Done!\t(" << t_elapse.count() << "ms)\n";
            
            cout << "\t Constructing KD-Tree....... " << flush;
            t_start = high_resolution_clock::now();
            ptcloud = KNN::NearestNeighbor{wavefront}; // TODO: fix design
            t_end = high_resolution_clock::now();
            t_elapse = t_end - t_start;
            cout << "Done!\t(" << t_elapse.count() << "ms)\n";
            cout << endl;
            continue;
            
        } else if (cmd_keyword == "help") {
            cout << "\n";
            PrintHelp();
            cout << "Command Keyword:\n"
            << setw(15) << "exit:" << "\tEnd this program. (Alternative: CTRL+D).\n"
            << setw(15) << "help:" << "\tDisplay this help interface.\n"
            << setw(15) << "kvalue [val=5]:" << "\tCheck [or set] k-value (search k nearest points).\n"
            << setw(15) << "loadobj file:" << "\tLoad point cloud as Wavefront OBJ file.\n"
            << setw(15) << "query vector:" << "\tSpecify a proximity vector of n-dimension.\n"
            << setw(15) << "quit:" << "\tEnd this program. (Alternative: CTRL+D).\n"
            << endl;
            continue;
            
        } else if (cmd_keyword == "quit" or cmd_keyword == "exit") {
            cout << endl;
            break;
        
        } else {
            cout << "\t Command not recognized\n" << endl;
            continue;
        }
    } // END while loop
}


void PrintHelp() {
    std::cout <<
    "knnsearch will search for some k nearest points within point cloud using\n"
    "given query vector. Only quantative-valued point cloud (training data) and\n"
    "query vectors (test set) are supported.\n\n"
    "A few caveats:\n"
    "Currently, only Wavefront OBJ file format are supported for training set.\n"
    "Currently, only 3-dimension data are supported.\n\n";
};
