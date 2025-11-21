cmake_minimum_required(VERSION 3.16)
cmake_policy(VERSION 3.16)


project (testable
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
add_library(testable-server ${SERVER_SOURCE_FILES})
add_library(Testable::Server ALIAS testable-server)
target_include_directories(testable-server
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
		${mosquitto_INCLUDE_DIRS}
		${rapidJSON_INCLUDE_DIRS}
)
target_link_libraries(testable-server
	PUBLIC
		PkgConfig::mosquitto
		Boost::thread
		Boost::chrono
)

# client lib
add_library(testable-client ${CLIENT_SOURCE_FILES})
add_library(Testable::Client ALIAS testable-client)
target_include_directories(testable-client
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
		${rapidJSON_INCLUDE_DIRS}
)
target_link_libraries(testable-client
	PUBLIC
		PkgConfig::mosquitto
		Boost::thread
		Boost::chrono
)

# example client
add_executable(testable-client-demo examples/client_main.cpp)
target_link_libraries(testable-client-demo
	PRIVATE
		Testable::Client
)

add_executable(testable-server-demo examples/server_main.cpp)
target_link_libraries(testable-server-demo
	PRIVATE
		Testable::Server
)

add_executable(testable-discovery-example examples/discovery_example.cpp)
target_link_libraries(testable-discovery-example
	PRIVATE
		Testable::Client
)

add_executable(testable-discovery-publisher examples/discovery_publisher.cpp)
target_link_libraries(testable-discovery-publisher
	PRIVATE
		Testable::Client
)

set_target_properties(
	testable-client
	testable-server
	testable-client-demo
	testable-server-demo
	testable-discovery-publisher
	testable-discovery-example
	PROPERTIES
		CXX_STANDARD 17 # use 17, if you can
		CXX_STANDARD_REQUIRED ON # use 17, I insist
		CXX_EXTENSIONS OFF # use c++17 not gnu++17
)

# help cmake find this
configure_package_config_file(
	${CMAKE_CURRENT_SOURCE_DIR}/cmake/Testable-config.cmake.in
	${CMAKE_CURRENT_BINARY_DIR}/Testable-config.cmake
	INSTALL_DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/Testable
	PATH_VARS CMAKE_INSTALL_INCLUDEDIR CMAKE_INSTALL_LIBDIR
)

# help cmake enforce version rules
write_basic_package_version_file(
	${CMAKE_CURRENT_SOURCE_DIR}/cmake/Testable-config-version.cmake
	VERSION 0.0.1
	COMPATIBILITY AnyNewerVersion
)

install(FILES
	${CMAKE_CURRENT_BINARY_DIR}/Testable-config.cmake
	${CMAKE_CURRENT_BINARY_DIR}/Testable-config-version.cmake
	DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/Testable
)

install(DIRECTORY
	${CMAKE_CURRENT_SOURCE_DIR}/include/Testable
	DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(TARGETS
	testable-server
	testable-client
	testable-server-demo
	testable-client-demo
	testable-discovery-example
	testable-discovery-publisher
	EXPORT TestableTargets
	ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR} # .a files
	LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR} # .so files
	RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} # executables
)

install(EXPORT
	TestableTargets
	FILE Testable-targets.cmake
	DESTINATION ${CMAKE_INSTALL_DATADIR}/cmake/Testable
	NAMESPACE Testable::
)

export (EXPORT TestableTargets
	FILE ${CMAKE_CURRENT_BINARY_DIR}/Testable-targets.cmake
	NAMESPACE Testable::
)