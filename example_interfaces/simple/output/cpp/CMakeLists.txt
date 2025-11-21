cmake_minimum_required(VERSION 3.16)
cmake_policy(VERSION 3.16)


project (simple
	LANGUAGES CXX
	VERSION 0.0.1)

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

# more secure code
set (CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(PkgConfig REQUIRED)
find_package(RapidJSON REQUIRED)
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
add_library(simple-server ${SERVER_SOURCE_FILES})
add_library(Simple::Server ALIAS simple-server)
target_include_directories(simple-server
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
		${mosquitto_INCLUDE_DIRS}
		${rapidJSON_INCLUDE_DIRS}
)
target_link_libraries(simple-server
	PUBLIC
		PkgConfig::mosquitto
)

# client lib
add_library(simple-client ${CLIENT_SOURCE_FILES})
add_library(Simple::Client ALIAS simple-client)
target_include_directories(simple-client
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
		${rapidJSON_INCLUDE_DIRS}
)
target_link_libraries(simple-client
	PUBLIC
		PkgConfig::mosquitto
)

# example client
add_executable(simple-client-demo examples/client_main.cpp)
target_link_libraries(simple-client-demo
	PRIVATE
		Simple::Client
)

add_executable(simple-server-demo examples/server_main.cpp)
target_link_libraries(simple-server-demo
	PRIVATE
		Simple::Server
)

add_executable(simple-discovery-example examples/discovery_example.cpp)
target_link_libraries(simple-discovery-example
	PRIVATE
		Simple::Client
)

add_executable(simple-discovery-publisher examples/discovery_publisher.cpp)
target_link_libraries(simple-discovery-publisher
	PRIVATE
		Simple::Client
)

set_target_properties(
	simple-client
	simple-server
	simple-client-demo
	simple-server-demo
	simple-discovery-publisher
	simple-discovery-example
	PROPERTIES
		CXX_STANDARD 17 # use 17, if you can
		CXX_STANDARD_REQUIRED ON # use 17, I insist
		CXX_EXTENSIONS OFF # use c++17 not gnu++17
)

# help cmake find this
configure_package_config_file(
	${CMAKE_CURRENT_SOURCE_DIR}/cmake/Simple-config.cmake.in
	${CMAKE_CURRENT_BINARY_DIR}/Simple-config.cmake
	INSTALL_DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/Simple
	PATH_VARS CMAKE_INSTALL_INCLUDEDIR CMAKE_INSTALL_LIBDIR
)

# help cmake enforce version rules
write_basic_package_version_file(
	${CMAKE_CURRENT_SOURCE_DIR}/cmake/Simple-config-version.cmake
	VERSION 0.0.1
	COMPATIBILITY AnyNewerVersion
)

install(FILES
	${CMAKE_CURRENT_BINARY_DIR}/Simple-config.cmake
	${CMAKE_CURRENT_BINARY_DIR}/Simple-config-version.cmake
	DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/Simple
)

install(DIRECTORY
	${CMAKE_CURRENT_SOURCE_DIR}/include/Simple
	DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(TARGETS
	simple-server
	simple-client
	simple-server-demo
	simple-client-demo
	simple-discovery-example
	simple-discovery-publisher
	EXPORT SimpleTargets
	ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR} # .a files
	LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR} # .so files
	RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} # executables
)

install(EXPORT
	SimpleTargets
	FILE Simple-targets.cmake
	DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/Simple
	NAMESPACE Simple::
)

export (EXPORT SimpleTargets
	FILE ${CMAKE_CURRENT_BINARY_DIR}/Simple-targets.cmake
	NAMESPACE Simple::
)