cmake_minimum_required(VERSION 3.16)

project (weather)
set(CMAKE_CXX_STANDARD 11) 

include_directories(include)
 
set(CLIENT_SOURCE_FILES src/broker.cpp src/client.cpp src/property_structs.cpp src/structs.cpp )
set(SERVER_SOURCE_FILES src/broker.cpp src/property_structs.cpp src/server.cpp src/structs.cpp )

add_library(lib-weather-server ${SERVER_SOURCE_FILES})
add_library(lib-weather-client ${CLIENT_SOURCE_FILES})

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

add_executable(weather-client-demo examples/client_main.cpp)
target_link_libraries(weather-client-demo PUBLIC lib-weather-client)
target_link_libraries(weather-client-demo PUBLIC mosquitto)
target_link_libraries(weather-client-demo PUBLIC boost_thread)
target_link_libraries(weather-client-demo PUBLIC boost_chrono)
target_link_libraries(weather-client-demo PRIVATE Threads::Threads)

add_executable(weather-server-demo examples/server_main.cpp)
target_link_libraries(weather-server-demo PUBLIC lib-weather-server)
target_link_libraries(weather-server-demo PUBLIC mosquitto)
target_link_libraries(weather-server-demo PUBLIC boost_thread)
target_link_libraries(weather-server-demo PRIVATE Threads::Threads)

# Install rules
install(TARGETS lib-weather-server lib-weather-client
	ARCHIVE DESTINATION lib
	LIBRARY DESTINATION lib
	RUNTIME DESTINATION bin)
install(TARGETS weather-client-demo weather-server-demo
	RUNTIME DESTINATION bin)
install(DIRECTORY include/ DESTINATION include)

# CPack configuration
set(CPACK_PACKAGE_NAME "weather-${CMAKE_SYSTEM_PROCESSOR}")
set(CPACK_PACKAGE_VERSION "0.1.2")
set(CPACK_GENERATOR "TGZ")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Current conditions, daily and hourly forecasts from the NWS API")
include(CPack)