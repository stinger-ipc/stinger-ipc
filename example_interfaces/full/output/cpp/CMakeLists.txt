cmake_minimum_required(VERSION 3.23)

project (Example)
set(CMAKE_CXX_STANDARD 11) 

include_directories(include)
 
set(SOURCE_FILES src/broker.cpp src/client.cpp src/server.cpp )

add_library(lib-Example ${SOURCE_FILES})

add_executable(client-demo examples/client_main.cpp)
target_link_libraries(client-demo PUBLIC lib-Example)
target_link_libraries(client-demo PUBLIC mosquitto)

add_executable(server-demo examples/server_main.cpp)
target_link_libraries(server-demo PUBLIC lib-Example)
target_link_libraries(server-demo PUBLIC mosquitto)