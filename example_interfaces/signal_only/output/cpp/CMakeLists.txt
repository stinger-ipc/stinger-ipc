cmake_minimum_required(VERSION 3.16)

project (SignalOnly)
set(CMAKE_CXX_STANDARD 11) 

include_directories(include)
 
set(SOURCE_FILES src/broker.cpp src/client.cpp src/server.cpp )

add_library(lib-SignalOnly ${SOURCE_FILES})

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

add_executable(client-demo examples/client_main.cpp)
target_link_libraries(client-demo PUBLIC lib-SignalOnly)
target_link_libraries(client-demo PUBLIC mosquitto)
target_link_libraries(client-demo PUBLIC boost_thread)
target_link_libraries(client-demo PRIVATE Threads::Threads)

add_executable(server-demo examples/server_main.cpp)
target_link_libraries(server-demo PUBLIC lib-SignalOnly)
target_link_libraries(server-demo PUBLIC mosquitto)
target_link_libraries(server-demo PUBLIC boost_thread)
target_link_libraries(server-demo PRIVATE Threads::Threads)