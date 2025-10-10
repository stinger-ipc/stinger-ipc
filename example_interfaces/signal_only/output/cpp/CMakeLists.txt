cmake_minimum_required(VERSION 3.16)

project (signal-only-ipc)
set(CMAKE_CXX_STANDARD 11) 

include_directories(include)
 
set(CLIENT_SOURCE_FILES src/broker.cpp src/client.cpp src/conversions.cpp src/discovery.cpp src/method_payloads.cpp src/property_structs.cpp src/signal_payloads.cpp src/structs.cpp )
set(SERVER_SOURCE_FILES src/broker.cpp src/conversions.cpp src/discovery.cpp src/method_payloads.cpp src/property_structs.cpp src/server.cpp src/signal_payloads.cpp src/structs.cpp )

add_library(lib-signal-only-ipc-server ${SERVER_SOURCE_FILES})
add_library(lib-signal-only-ipc-client ${CLIENT_SOURCE_FILES})

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

add_executable(signal-only-ipc-client-demo examples/client_main.cpp)
target_link_libraries(signal-only-ipc-client-demo PUBLIC lib-signal-only-ipc-client)
target_link_libraries(signal-only-ipc-client-demo PUBLIC mosquitto)
target_link_libraries(signal-only-ipc-client-demo PUBLIC boost_thread)
target_link_libraries(signal-only-ipc-client-demo PUBLIC boost_chrono)
target_link_libraries(signal-only-ipc-client-demo PRIVATE Threads::Threads)

add_executable(signal-only-ipc-server-demo examples/server_main.cpp)
target_link_libraries(signal-only-ipc-server-demo PUBLIC lib-signal-only-ipc-server)
target_link_libraries(signal-only-ipc-server-demo PUBLIC mosquitto)
target_link_libraries(signal-only-ipc-server-demo PUBLIC boost_thread)
target_link_libraries(signal-only-ipc-server-demo PRIVATE Threads::Threads)

add_executable(signal-only-ipc-discovery-example examples/discovery_example.cpp)
target_link_libraries(signal-only-ipc-discovery-example PUBLIC lib-signal-only-ipc-client)
target_link_libraries(signal-only-ipc-discovery-example PUBLIC mosquitto)
target_link_libraries(signal-only-ipc-discovery-example PUBLIC boost_thread)
target_link_libraries(signal-only-ipc-discovery-example PUBLIC boost_chrono)
target_link_libraries(signal-only-ipc-discovery-example PRIVATE Threads::Threads)

add_executable(signal-only-ipc-discovery-publisher examples/discovery_publisher.cpp)
target_link_libraries(signal-only-ipc-discovery-publisher PUBLIC lib-signal-only-ipc-client)
target_link_libraries(signal-only-ipc-discovery-publisher PUBLIC mosquitto)
target_link_libraries(signal-only-ipc-discovery-publisher PUBLIC boost_thread)
target_link_libraries(signal-only-ipc-discovery-publisher PUBLIC boost_chrono)
target_link_libraries(signal-only-ipc-discovery-publisher PRIVATE Threads::Threads)

# Install rules
install(TARGETS lib-signal-only-ipc-server lib-signal-only-ipc-client
	ARCHIVE DESTINATION lib
	LIBRARY DESTINATION lib
	RUNTIME DESTINATION bin)
install(TARGETS signal-only-ipc-client-demo signal-only-ipc-server-demo
	RUNTIME DESTINATION bin)
install(DIRECTORY include/ DESTINATION include)

# CPack configuration
set(CPACK_PACKAGE_NAME "signal-only-ipc-${CMAKE_SYSTEM_PROCESSOR}")
set(CPACK_PACKAGE_VERSION "0.0.1")
set(CPACK_GENERATOR "TGZ")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "")
include(CPack)