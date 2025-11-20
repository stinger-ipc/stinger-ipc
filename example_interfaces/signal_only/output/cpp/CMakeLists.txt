cmake_minimum_required(VERSION 3.16)
cmake_policy(VERSION 3.16)


project (signal-only
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
add_library(signal-only-server ${SERVER_SOURCE_FILES})
add_library(SignalOnly::Server ALIAS signal-only-server)
target_include_directories(signal-only-server
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
		${mosquitto_INCLUDE_DIRS}
		${rapidJSON_INCLUDE_DIRS}
)
target_link_libraries(signal-only-server
	PUBLIC
		PkgConfig::mosquitto
		Boost::thread
)

# client lib
add_library(signal-only-client ${CLIENT_SOURCE_FILES})
add_library(SignalOnly::Client ALIAS signal-only-client)
target_include_directories(signal-only-client
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
		${rapidJSON_INCLUDE_DIRS}
)
target_link_libraries(signal-only-client
	PUBLIC
		PkgConfig::mosquitto
		Boost::thread
)

# example client
add_executable(signal-only-client-demo examples/client_main.cpp)
target_link_libraries(signal-only-client-demo
	PRIVATE
		SignalOnly::Client
)

add_executable(signal-only-server-demo examples/server_main.cpp)
target_link_libraries(signal-only-server-demo
	PRIVATE
		SignalOnly::Server
)

add_executable(signal-only-discovery-example examples/discovery_example.cpp)
target_link_libraries(signal-only-discovery-example
	PRIVATE
		SignalOnly::Client
)

add_executable(signal-only-discovery-publisher examples/discovery_publisher.cpp)
target_link_libraries(signal-only-discovery-publisher
	PRIVATE
		SignalOnly::Client
)

set_target_properties(
	signal-only-client
	signal-only-server
	signal-only-client-demo
	signal-only-server-demo
	signal-only-discovery-publisher
	signal-only-discovery-example
	PROPERTIES
		CXX_STANDARD 17 # use 17, if you can
		CXX_STANDARD_REQUIRED ON # use 17, I insist
		CXX_EXTENSIONS OFF # use c++17 not gnu++17
)

# help cmake find this
configure_package_config_file(
	${CMAKE_CURRENT_SOURCE_DIR}/cmake/SignalOnly-config.cmake.in
	${CMAKE_CURRENT_BINARY_DIR}/SignalOnly-config.cmake
	INSTALL_DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/SignalOnly
	PATH_VARS CMAKE_INSTALL_INCLUDEDIR CMAKE_INSTALL_LIBDIR
)

# help cmake enforce version rules
write_basic_package_version_file(
	${CMAKE_CURRENT_SOURCE_DIR}/cmake/SignalOnly-config-version.cmake
	VERSION 0.0.1
	COMPATIBILITY AnyNewerVersion
)

install(FILES
	${CMAKE_CURRENT_BINARY_DIR}/SignalOnly-config.cmake
	${CMAKE_CURRENT_BINARY_DIR}/SignalOnly-config-version.cmake
	DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/SignalOnly
)

install(DIRECTORY
	${CMAKE_CURRENT_SOURCE_DIR}/include/SignalOnly
	DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(TARGETS
	signal-only-server
	signal-only-client
	signal-only-server-demo
	signal-only-client-demo
	signal-only-discovery-example
	signal-only-discovery-publisher
	EXPORT SignalOnlyTargets
	ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR} # .a files
	LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR} # .so files
	RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} # executables
)

install(EXPORT
	SignalOnlyTargets
	FILE SignalOnly-targets.cmake
	DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/SignalOnly
	NAMESPACE SignalOnly::
)

export (EXPORT SignalOnlyTargets
	FILE ${CMAKE_CURRENT_BINARY_DIR}/SignalOnly-targets.cmake
	NAMESPACE SignalOnly::
)