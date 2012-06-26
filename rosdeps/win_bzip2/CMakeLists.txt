cmake_minimum_required(VERSION 2.8)
# We are using a .def file instead of exports.
#cmake_minimum_required(VERSION 2.8.6)

#include (GenerateExportHeader) # Needs 2.8.6

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)

set(BUILD_SHARED_LIBS ON)
set(LIBRARY_SOURCES
        src/blocksort.c
		src/bzlib.c
		src/compress.c
		src/crctable.c
		src/decompress.c
		src/huffman.c
		src/randtable.c
		src/libbz2.def
		)
		
add_definitions(-DWIN32 -D_FILE_OFFSET_BITS=64 -nologo)
add_library(bzip2 ${LIBRARY_SOURCES})
add_subdirectory(src)
add_subdirectory(cmake)

install(TARGETS bzip2 
        RUNTIME DESTINATION bin
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        )
if( NOT CMAKE_BUILD_TYPE STREQUAL "Release")
  install(FILES ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/bzip2.pdb DESTINATION bin)
endif() 

#GENERATE_EXPORT_HEADER( bzip2
#             BASE_NAME bzip2
#             EXPORT_MACRO_NAME bzip2_EXPORT
#             EXPORT_FILE_NAME bzip2_Export.h
#             STATIC_DEFINE bzip2_BUILT_AS_STATIC
#)
