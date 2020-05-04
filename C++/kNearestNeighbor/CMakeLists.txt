cmake_minimum_required(VERSION 3.10)

# Set the project name and version
project(knnsearch 
		VERSION 1.0.0 
		DESCRIPTION "k-nearest neighbor search"
		LANGUAGES CXX
		)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
#set(CMAKE_CXX_STANDARD_REQUIRED ON)
#add_compile_options(-Wall -Wextra -pedantic -O3)

# Specify where runtime output will be located
#set( CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)


# Specify our include directories and also system include directory
include_directories( include )

find_package(Boost 1.60 REQUIRED COMPONENTS program_options)
include_directories(${Boost_INCLUDE_DIR})

add_subdirectory(src)
