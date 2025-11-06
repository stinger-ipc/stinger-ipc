cmake_minimum_required(VERSION 3.16)
cmake_policy(VERSION 3.16)


project (test-able
	LANGUAGES CXX
	VERSION 0.0.1)

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

# more secure code
set (CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(PkgConfig REQUIRED)
find_package(RapidJSON REQUIRED)
find_package(Boost CONFIG REQUIRED COMPONENTS thread chrono)
pkg_check_modules(mosquitto REQUIRED libmosquitto)

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
add_library(test-able-server ${SERVER_SOURCE_FILES})
add_library(TestAble::Server ALIAS test-able-server)
target_include_directories(test-able-server
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
		${mosquitto_INCLUDE_DIRS}
		${rapidJSON_INCLUDE_DIRS}
)
target_link_libraries(test-able-server
	PUBLIC
		mosquitto
		Boost::thread
)

# client lib
add_library(test-able-client ${CLIENT_SOURCE_FILES})
add_library(TestAble::Client ALIAS test-able-client)
target_include_directories(test-able-client
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
		${mosquitto_INCLUDE_DIRS}
		${rapidJSON_INCLUDE_DIRS}
)
target_link_libraries(test-able-client
	PUBLIC
		mosquitto
		Boost::thread
)

# example client
add_executable(test-able-client-demo examples/client_main.cpp)
target_link_libraries(test-able-client-demo
	PRIVATE
		TestAble::Client
)

add_executable(test-able-server-demo examples/server_main.cpp)
target_link_libraries(test-able-server-demo
	PRIVATE
		TestAble::Server
)

add_executable(test-able-discovery-example examples/discovery_example.cpp)
target_link_libraries(test-able-discovery-example
	PRIVATE
		TestAble::Client
)

add_executable(test-able-discovery-publisher examples/discovery_publisher.cpp)
target_link_libraries(test-able-discovery-publisher
	PRIVATE
		TestAble::Client
)

set_target_properties(
	test-able-client
	test-able-server
	test-able-client-demo
	test-able-server-demo
	test-able-discovery-publisher
	test-able-discovery-example
	PROPERTIES
		CXX_STANDARD 11 # use 17, if you can
		CXX_STANDARD_REQUIRED ON # use 17, I insist
		CXX_EXTENSIONS OFF # use c++17 not gnu++17
)

# help cmake find this
configure_package_config_file(
	${CMAKE_CURRENT_SOURCE_DIR}/cmake/TestAble-config.cmake.in
	${CMAKE_CURRENT_BINARY_DIR}/TestAble-config.cmake
	INSTALL_DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/TestAble
	PATH_VARS CMAKE_INSTALL_INCLUDEDIR CMAKE_INSTALL_LIBDIR
)

# help cmake enforce version rules
write_basic_package_version_file(
	${CMAKE_CURRENT_SOURCE_DIR}/cmake/TestAble-config-version.cmake
	VERSION 0.0.1
	COMPATIBILITY AnyNewerVersion
)

install(FILES
	${CMAKE_CURRENT_BINARY_DIR}/TestAble-config.cmake
	${CMAKE_CURRENT_BINARY_DIR}/TestAble-config-version.cmake
	DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/TestAble
)

install(DIRECTORY
	${CMAKE_CURRENT_SOURCE_DIR}/include/TestAble
	DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(TARGETS
	test-able-server
	test-able-client
	test-able-server-demo
	test-able-client-demo
	test-able-discovery-example
	test-able-discovery-publisher
	EXPORT TestAbleTargets
	ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR} # .a files
	LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR} # .so files
	RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} # executables
)

install(EXPORT
	TestAbleTargets
	FILE TestAble-targets.cmake
	DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/TestAble
	NAMESPACE TestAble::
)

export (EXPORT TestAbleTargets
	FILE ${CMAKE_CURRENT_BINARY_DIR}/TestAble-targets.cmake
	NAMESPACE TestAble::
)