cmake_minimum_required(VERSION 3.16)

project (weather-ipc)
set(CMAKE_CXX_STANDARD 11) 

include_directories(include)
 
set(CLIENT_SOURCE_FILES src/broker.cpp src/client.cpp src/conversions.cpp src/discovery.cpp src/interface_exceptions.cpp src/method_payloads.cpp src/property_structs.cpp src/signal_payloads.cpp src/structs.cpp )
set(SERVER_SOURCE_FILES src/broker.cpp src/conversions.cpp src/discovery.cpp src/interface_exceptions.cpp src/method_payloads.cpp src/property_structs.cpp src/server.cpp src/signal_payloads.cpp src/structs.cpp )

add_library(lib-weather-ipc-server ${SERVER_SOURCE_FILES})
add_library(lib-weather-ipc-client ${CLIENT_SOURCE_FILES})

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

add_executable(weather-ipc-client-demo examples/client_main.cpp)
target_link_libraries(weather-ipc-client-demo PUBLIC lib-weather-ipc-client)
target_link_libraries(weather-ipc-client-demo PUBLIC mosquitto)
target_link_libraries(weather-ipc-client-demo PUBLIC boost_thread)
target_link_libraries(weather-ipc-client-demo PUBLIC boost_chrono)
target_link_libraries(weather-ipc-client-demo PRIVATE Threads::Threads)

add_executable(weather-ipc-server-demo examples/server_main.cpp)
target_link_libraries(weather-ipc-server-demo PUBLIC lib-weather-ipc-server)
target_link_libraries(weather-ipc-server-demo PUBLIC mosquitto)
target_link_libraries(weather-ipc-server-demo PUBLIC boost_thread)
target_link_libraries(weather-ipc-server-demo PRIVATE Threads::Threads)

add_executable(weather-ipc-discovery-example examples/discovery_example.cpp)
target_link_libraries(weather-ipc-discovery-example PUBLIC lib-weather-ipc-client)
target_link_libraries(weather-ipc-discovery-example PUBLIC mosquitto)
target_link_libraries(weather-ipc-discovery-example PUBLIC boost_thread)
target_link_libraries(weather-ipc-discovery-example PUBLIC boost_chrono)
target_link_libraries(weather-ipc-discovery-example PRIVATE Threads::Threads)

add_executable(weather-ipc-discovery-publisher examples/discovery_publisher.cpp)
target_link_libraries(weather-ipc-discovery-publisher PUBLIC lib-weather-ipc-client)
target_link_libraries(weather-ipc-discovery-publisher PUBLIC mosquitto)
target_link_libraries(weather-ipc-discovery-publisher PUBLIC boost_thread)
target_link_libraries(weather-ipc-discovery-publisher PUBLIC boost_chrono)
target_link_libraries(weather-ipc-discovery-publisher PRIVATE Threads::Threads)

# Install rules
install(TARGETS lib-weather-ipc-server lib-weather-ipc-client
	ARCHIVE DESTINATION lib
	LIBRARY DESTINATION lib
	RUNTIME DESTINATION bin)
install(TARGETS weather-ipc-client-demo weather-ipc-server-demo
	RUNTIME DESTINATION bin)
install(DIRECTORY include/ DESTINATION include)

# CPack configuration
set(CPACK_PACKAGE_NAME "weather-ipc-${CMAKE_SYSTEM_PROCESSOR}")
set(CPACK_PACKAGE_VERSION "0.1.2")
set(CPACK_GENERATOR "TGZ")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Current conditions, daily and hourly forecasts from the NWS API")
include(CPack)