cmake_minimum_required(VERSION 3.16)

project (Full)
set(CMAKE_CXX_STANDARD 11) 

include_directories(include)
 
set(CLIENT_SOURCE_FILES src/broker.cpp src/client.cpp src/discovery.cpp src/property_structs.cpp src/structs.cpp )
set(SERVER_SOURCE_FILES src/broker.cpp src/discovery.cpp src/property_structs.cpp src/server.cpp src/structs.cpp )

add_library(lib-Full-server ${SERVER_SOURCE_FILES})
add_library(lib-Full-client ${CLIENT_SOURCE_FILES})

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

add_executable(Full-client-demo examples/client_main.cpp)
target_link_libraries(Full-client-demo PUBLIC lib-Full-client)
target_link_libraries(Full-client-demo PUBLIC mosquitto)
target_link_libraries(Full-client-demo PUBLIC boost_thread)
target_link_libraries(Full-client-demo PUBLIC boost_chrono)
target_link_libraries(Full-client-demo PRIVATE Threads::Threads)

add_executable(Full-server-demo examples/server_main.cpp)
target_link_libraries(Full-server-demo PUBLIC lib-Full-server)
target_link_libraries(Full-server-demo PUBLIC mosquitto)
target_link_libraries(Full-server-demo PUBLIC boost_thread)
target_link_libraries(Full-server-demo PRIVATE Threads::Threads)

add_executable(Full-discovery-example examples/discovery_example.cpp)
target_link_libraries(Full-discovery-example PUBLIC lib-Full-client)
target_link_libraries(Full-discovery-example PUBLIC mosquitto)
target_link_libraries(Full-discovery-example PUBLIC boost_thread)
target_link_libraries(Full-discovery-example PUBLIC boost_chrono)
target_link_libraries(Full-discovery-example PRIVATE Threads::Threads)

add_executable(Full-discovery-publisher examples/discovery_publisher.cpp)
target_link_libraries(Full-discovery-publisher PUBLIC lib-Full-client)
target_link_libraries(Full-discovery-publisher PUBLIC mosquitto)
target_link_libraries(Full-discovery-publisher PUBLIC boost_thread)
target_link_libraries(Full-discovery-publisher PUBLIC boost_chrono)
target_link_libraries(Full-discovery-publisher PRIVATE Threads::Threads)

# Install rules
install(TARGETS lib-Full-server lib-Full-client
	ARCHIVE DESTINATION lib
	LIBRARY DESTINATION lib
	RUNTIME DESTINATION bin)
install(TARGETS Full-client-demo Full-server-demo
	RUNTIME DESTINATION bin)
install(DIRECTORY include/ DESTINATION include)

# CPack configuration
set(CPACK_PACKAGE_NAME "Full-${CMAKE_SYSTEM_PROCESSOR}")
set(CPACK_PACKAGE_VERSION "0.0.1")
set(CPACK_GENERATOR "TGZ")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Example StingerAPI interface which demonstrates most features.")
include(CPack)