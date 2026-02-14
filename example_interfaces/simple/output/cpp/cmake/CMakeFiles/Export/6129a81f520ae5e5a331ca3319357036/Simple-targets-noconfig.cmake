#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Simple::simple-server" for configuration ""
set_property(TARGET Simple::simple-server APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(Simple::simple-server PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_NOCONFIG "CXX"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libsimple-server.a"
  )

list(APPEND _cmake_import_check_targets Simple::simple-server )
list(APPEND _cmake_import_check_files_for_Simple::simple-server "${_IMPORT_PREFIX}/lib/libsimple-server.a" )

# Import target "Simple::simple-client" for configuration ""
set_property(TARGET Simple::simple-client APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(Simple::simple-client PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_NOCONFIG "CXX"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libsimple-client.a"
  )

list(APPEND _cmake_import_check_targets Simple::simple-client )
list(APPEND _cmake_import_check_files_for_Simple::simple-client "${_IMPORT_PREFIX}/lib/libsimple-client.a" )

# Import target "Simple::simple-server-demo" for configuration ""
set_property(TARGET Simple::simple-server-demo APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(Simple::simple-server-demo PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/bin/simple-server-demo"
  )

list(APPEND _cmake_import_check_targets Simple::simple-server-demo )
list(APPEND _cmake_import_check_files_for_Simple::simple-server-demo "${_IMPORT_PREFIX}/bin/simple-server-demo" )

# Import target "Simple::simple-client-demo" for configuration ""
set_property(TARGET Simple::simple-client-demo APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(Simple::simple-client-demo PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/bin/simple-client-demo"
  )

list(APPEND _cmake_import_check_targets Simple::simple-client-demo )
list(APPEND _cmake_import_check_files_for_Simple::simple-client-demo "${_IMPORT_PREFIX}/bin/simple-client-demo" )

# Import target "Simple::simple-discovery-example" for configuration ""
set_property(TARGET Simple::simple-discovery-example APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(Simple::simple-discovery-example PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/bin/simple-discovery-example"
  )

list(APPEND _cmake_import_check_targets Simple::simple-discovery-example )
list(APPEND _cmake_import_check_files_for_Simple::simple-discovery-example "${_IMPORT_PREFIX}/bin/simple-discovery-example" )

# Import target "Simple::simple-discovery-publisher" for configuration ""
set_property(TARGET Simple::simple-discovery-publisher APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(Simple::simple-discovery-publisher PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/bin/simple-discovery-publisher"
  )

list(APPEND _cmake_import_check_targets Simple::simple-discovery-publisher )
list(APPEND _cmake_import_check_files_for_Simple::simple-discovery-publisher "${_IMPORT_PREFIX}/bin/simple-discovery-publisher" )

# Import target "Simple::stinger_utils" for configuration ""
set_property(TARGET Simple::stinger_utils APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(Simple::stinger_utils PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_NOCONFIG "CXX"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libstinger_utils.a"
  )

list(APPEND _cmake_import_check_targets Simple::stinger_utils )
list(APPEND _cmake_import_check_files_for_Simple::stinger_utils "${_IMPORT_PREFIX}/lib/libstinger_utils.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
