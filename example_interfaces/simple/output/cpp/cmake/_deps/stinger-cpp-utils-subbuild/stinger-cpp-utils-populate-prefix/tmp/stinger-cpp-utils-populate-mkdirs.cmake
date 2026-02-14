# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION ${CMAKE_VERSION}) # this file comes with cmake

# If CMAKE_DISABLE_SOURCE_CHANGES is set to true and the source directory is an
# existing directory in our source tree, calling file(MAKE_DIRECTORY) on it
# would cause a fatal error, even though it would be a no-op.
if(NOT EXISTS "/home/jacob/projects/stinger-ipc/example_interfaces/simple/output/cpp/cmake/_deps/stinger-cpp-utils-src")
  file(MAKE_DIRECTORY "/home/jacob/projects/stinger-ipc/example_interfaces/simple/output/cpp/cmake/_deps/stinger-cpp-utils-src")
endif()
file(MAKE_DIRECTORY
  "/home/jacob/projects/stinger-ipc/example_interfaces/simple/output/cpp/cmake/_deps/stinger-cpp-utils-build"
  "/home/jacob/projects/stinger-ipc/example_interfaces/simple/output/cpp/cmake/_deps/stinger-cpp-utils-subbuild/stinger-cpp-utils-populate-prefix"
  "/home/jacob/projects/stinger-ipc/example_interfaces/simple/output/cpp/cmake/_deps/stinger-cpp-utils-subbuild/stinger-cpp-utils-populate-prefix/tmp"
  "/home/jacob/projects/stinger-ipc/example_interfaces/simple/output/cpp/cmake/_deps/stinger-cpp-utils-subbuild/stinger-cpp-utils-populate-prefix/src/stinger-cpp-utils-populate-stamp"
  "/home/jacob/projects/stinger-ipc/example_interfaces/simple/output/cpp/cmake/_deps/stinger-cpp-utils-subbuild/stinger-cpp-utils-populate-prefix/src"
  "/home/jacob/projects/stinger-ipc/example_interfaces/simple/output/cpp/cmake/_deps/stinger-cpp-utils-subbuild/stinger-cpp-utils-populate-prefix/src/stinger-cpp-utils-populate-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/home/jacob/projects/stinger-ipc/example_interfaces/simple/output/cpp/cmake/_deps/stinger-cpp-utils-subbuild/stinger-cpp-utils-populate-prefix/src/stinger-cpp-utils-populate-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/home/jacob/projects/stinger-ipc/example_interfaces/simple/output/cpp/cmake/_deps/stinger-cpp-utils-subbuild/stinger-cpp-utils-populate-prefix/src/stinger-cpp-utils-populate-stamp${cfgdir}") # cfgdir has leading slash
endif()
