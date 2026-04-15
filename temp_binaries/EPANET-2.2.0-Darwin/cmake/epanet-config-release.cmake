#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "epanet2" for configuration "Release"
set_property(TARGET epanet2 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(epanet2 PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libepanet2.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libepanet2.dylib"
  )

list(APPEND _cmake_import_check_targets epanet2 )
list(APPEND _cmake_import_check_files_for_epanet2 "${_IMPORT_PREFIX}/lib/libepanet2.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
