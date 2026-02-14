cmake_minimum_required(VERSION 3.16)
cmake_policy(VERSION 3.16)


project (weather
	LANGUAGES CXX
	VERSION 0.1.2)

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

# more secure code
set (CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(RapidJSON REQUIRED)

# Fetch stinger-cpp-utils dependency
include(FetchContent)
FetchContent_Declare(
	stinger-cpp-utils
	GIT_REPOSITORY https://github.com/stinger-ipc/stinger-cpp-utils.git
	GIT_TAG main  # or specify a specific tag/commit
)
FetchContent_MakeAvailable(stinger-cpp-utils)

set(CLIENT_SOURCE_FILES
	src/conversions.cpp
	src/discovery.cpp
	src/method_payloads.cpp
	src/property_structs.cpp
	src/server.cpp
	src/signal_payloads.cpp
	src/structs.cpp
	
)

set(SERVER_SOURCE_FILES
	src/client.cpp
	src/conversions.cpp
	src/discovery.cpp
	src/method_payloads.cpp
	src/property_structs.cpp
	src/signal_payloads.cpp
	src/structs.cpp
	
)

# server lib
add_library(weather-server ${SERVER_SOURCE_FILES})
add_library(Weather::Server ALIAS weather-server)
target_include_directories(weather-server
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
		${rapidJSON_INCLUDE_DIRS}
)
target_link_libraries(weather-server
	PUBLIC
		Stinger::Utils
)

# client lib
add_library(weather-client ${CLIENT_SOURCE_FILES})
add_library(Weather::Client ALIAS weather-client)
target_include_directories(weather-client
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
		${rapidJSON_INCLUDE_DIRS}
)
target_link_libraries(weather-client
	PUBLIC
		Stinger::Utils
)

# example client
add_executable(weather-client-demo examples/client_main.cpp)
target_link_libraries(weather-client-demo
	PRIVATE
		Weather::Client
)

add_executable(weather-server-demo examples/server_main.cpp)
target_link_libraries(weather-server-demo
	PRIVATE
		Weather::Server
)

add_executable(weather-discovery-example examples/discovery_example.cpp)
target_link_libraries(weather-discovery-example
	PRIVATE
		Weather::Client
)

add_executable(weather-discovery-publisher examples/discovery_publisher.cpp)
target_link_libraries(weather-discovery-publisher
	PRIVATE
		Weather::Client
)

set_target_properties(
	weather-client
	weather-server
	weather-client-demo
	weather-server-demo
	weather-discovery-publisher
	weather-discovery-example
	PROPERTIES
		CXX_STANDARD 17 # use 17, if you can
		CXX_STANDARD_REQUIRED ON # use 17, I insist
		CXX_EXTENSIONS OFF # use c++17 not gnu++17
)

# help cmake find this
configure_package_config_file(
	${CMAKE_CURRENT_SOURCE_DIR}/cmake/config.cmake.in
	${CMAKE_CURRENT_BINARY_DIR}/Weather-config.cmake
	INSTALL_DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/Weather
	PATH_VARS CMAKE_INSTALL_INCLUDEDIR CMAKE_INSTALL_LIBDIR
)

# help cmake enforce version rules
write_basic_package_version_file(
	${CMAKE_CURRENT_SOURCE_DIR}/cmake/Weather-config-version.cmake
	VERSION 0.1.2
	COMPATIBILITY AnyNewerVersion
)

install(FILES
	${CMAKE_CURRENT_BINARY_DIR}/Weather-config.cmake
	${CMAKE_CURRENT_BINARY_DIR}/Weather-config-version.cmake
	DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/Weather
)

install(DIRECTORY
	${CMAKE_CURRENT_SOURCE_DIR}/include/Weather
	DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(TARGETS
	weather-server
	weather-client
	weather-server-demo
	weather-client-demo
	weather-discovery-example
	weather-discovery-publisher
	stinger_utils
	EXPORT WeatherTargets
	ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR} # .a files
	LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR} # .so files
	RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} # executables
)

install(EXPORT
	WeatherTargets
	FILE Weather-targets.cmake
	DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/Weather
	NAMESPACE Weather::
)

export (EXPORT WeatherTargets
	FILE ${CMAKE_CURRENT_BINARY_DIR}/Weather-targets.cmake
	NAMESPACE Weather::
)