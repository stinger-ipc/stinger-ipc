cmake_minimum_required(VERSION 3.16)

project (SignalOnly)
set(CMAKE_CXX_STANDARD 11) 

include_directories(include)
 
set(CLIENT_SOURCE_FILES src/broker.cpp src/client.cpp src/property_structs.cpp src/structs.cpp )
set(SERVER_SOURCE_FILES src/broker.cpp src/property_structs.cpp src/server.cpp src/structs.cpp )

add_library(lib-SignalOnly-server ${SERVER_SOURCE_FILES})
add_library(lib-SignalOnly-client ${CLIENT_SOURCE_FILES})

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

add_executable(client-demo examples/client_main.cpp)
target_link_libraries(client-demo PUBLIC lib-SignalOnly-client)
target_link_libraries(client-demo PUBLIC mosquitto)
target_link_libraries(client-demo PUBLIC boost_thread)
target_link_libraries(client-demo PUBLIC boost_chrono)
target_link_libraries(client-demo PRIVATE Threads::Threads)

add_executable(server-demo examples/server_main.cpp)
target_link_libraries(server-demo PUBLIC lib-SignalOnly-server)
target_link_libraries(server-demo PUBLIC mosquitto)
target_link_libraries(server-demo PUBLIC boost_thread)
target_link_libraries(server-demo PRIVATE Threads::Threads)