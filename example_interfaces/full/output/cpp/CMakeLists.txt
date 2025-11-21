cmake_minimum_required(VERSION 3.16)
cmake_policy(VERSION 3.16)


project (full
	LANGUAGES CXX
	VERSION 0.0.1)

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

# more secure code
set (CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(PkgConfig REQUIRED)
find_package(RapidJSON REQUIRED)
find_package(Boost CONFIG REQUIRED COMPONENTS thread chrono)
pkg_check_modules(mosquitto REQUIRED libmosquitto IMPORTED_TARGET)

set(CLIENT_SOURCE_FILES
	src/broker.cpp
	src/client.cpp
	src/conversions.cpp
	src/discovery.cpp
	src/interface_exceptions.cpp
	src/method_payloads.cpp
	src/property_structs.cpp
	src/signal_payloads.cpp
	src/structs.cpp
	)

set(SERVER_SOURCE_FILES
	src/broker.cpp
	src/conversions.cpp
	src/discovery.cpp
	src/interface_exceptions.cpp
	src/method_payloads.cpp
	src/property_structs.cpp
	src/server.cpp
	src/signal_payloads.cpp
	src/structs.cpp
	)

# server lib
add_library(full-server ${SERVER_SOURCE_FILES})
add_library(Full::Server ALIAS full-server)
target_include_directories(full-server
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
		${mosquitto_INCLUDE_DIRS}
		${rapidJSON_INCLUDE_DIRS}
)
target_link_libraries(full-server
	PUBLIC
		PkgConfig::mosquitto
		Boost::thread
		Boost::chrono
)

# client lib
add_library(full-client ${CLIENT_SOURCE_FILES})
add_library(Full::Client ALIAS full-client)
target_include_directories(full-client
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
		${rapidJSON_INCLUDE_DIRS}
)
target_link_libraries(full-client
	PUBLIC
		PkgConfig::mosquitto
		Boost::thread
		Boost::chrono
)

# example client
add_executable(full-client-demo examples/client_main.cpp)
target_link_libraries(full-client-demo
	PRIVATE
		Full::Client
)

add_executable(full-server-demo examples/server_main.cpp)
target_link_libraries(full-server-demo
	PRIVATE
		Full::Server
)

add_executable(full-discovery-example examples/discovery_example.cpp)
target_link_libraries(full-discovery-example
	PRIVATE
		Full::Client
)

add_executable(full-discovery-publisher examples/discovery_publisher.cpp)
target_link_libraries(full-discovery-publisher
	PRIVATE
		Full::Client
)

set_target_properties(
	full-client
	full-server
	full-client-demo
	full-server-demo
	full-discovery-publisher
	full-discovery-example
	PROPERTIES
		CXX_STANDARD 17 # use 17, if you can
		CXX_STANDARD_REQUIRED ON # use 17, I insist
		CXX_EXTENSIONS OFF # use c++17 not gnu++17
)

# help cmake find this
configure_package_config_file(
	${CMAKE_CURRENT_SOURCE_DIR}/cmake/Full-config.cmake.in
	${CMAKE_CURRENT_BINARY_DIR}/Full-config.cmake
	INSTALL_DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/Full
	PATH_VARS CMAKE_INSTALL_INCLUDEDIR CMAKE_INSTALL_LIBDIR
)

# help cmake enforce version rules
write_basic_package_version_file(
	${CMAKE_CURRENT_SOURCE_DIR}/cmake/Full-config-version.cmake
	VERSION 0.0.1
	COMPATIBILITY AnyNewerVersion
)

install(FILES
	${CMAKE_CURRENT_BINARY_DIR}/Full-config.cmake
	${CMAKE_CURRENT_BINARY_DIR}/Full-config-version.cmake
	DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/Full
)

install(DIRECTORY
	${CMAKE_CURRENT_SOURCE_DIR}/include/Full
	DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(TARGETS
	full-server
	full-client
	full-server-demo
	full-client-demo
	full-discovery-example
	full-discovery-publisher
	EXPORT FullTargets
	ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR} # .a files
	LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR} # .so files
	RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} # executables
)

install(EXPORT
	FullTargets
	FILE Full-targets.cmake
	DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/Full
	NAMESPACE Full::
)

export (EXPORT FullTargets
	FILE ${CMAKE_CURRENT_BINARY_DIR}/Full-targets.cmake
	NAMESPACE Full::
)