set( SUPPORT_SRC
	BoundedVector.cpp
	CompleteBinaryTree.cpp
	Globals.cpp
	NearestNeighbor.cpp
	WavefrontObject.cpp
	)

add_executable( knnsearch kNearestNeighbor.cpp ${SUPPORT_SRC} )
target_compile_options( knnsearch PRIVATE -Wall -pedantic -O3 )

target_link_libraries( knnsearch LINK_PUBLIC ${Boost_LIBRARIES} )
set_target_properties( knnsearch PROPERTIES
	ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
	LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
	RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
	)
