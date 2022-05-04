cmake_minimum_required(VERSION 3.23)

project (Example)
set(CMAKE_CXX_STANDARD 11) 

include_directories(include)
 
set(SOURCE_FILES src/broker.cpp src/client.cpp src/server.cpp )

add_library(lib-Example ${SOURCE_FILES})


add_executable(clinet-demo examples/client_main.cpp)

target_link_libraries(clinet-demo PUBLIC lib-Example)
target_link_libraries(clinet-demo PUBLIC mosquitto)