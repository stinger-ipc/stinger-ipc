cmake_minimum_required(VERSION 3.23)

project (Example)
set(CMAKE_CXX_STANDARD 11) 

include_directories(include)
 
set(SOURCE_FILES )

add_library(lib-Example ${SOURCE_FILES})