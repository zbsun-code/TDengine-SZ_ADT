CMAKE_MINIMUM_REQUIRED(VERSION 3.0...3.20)
PROJECT(TDengine)

macro(check_odbc_requirement)
  find_package(FLEX)
  IF (NOT FLEX_FOUND)
    message(WARNING "you need to install flex first")
    return ()
  ENDIF ()
  IF (CMAKE_C_COMPILER_ID STREQUAL "GNU" AND CMAKE_C_COMPILER_VERSION VERSION_LESS 5.0.0)
    message(WARNING "gcc 4.8.0 will complain too much about flex-generated code, we just bypass building ODBC driver in such case")
    return ()
  ENDIF ()

  find_program(TD_ODBCINST_INSTALLED NAMES odbcinst)
  IF (NOT TD_ODBCINST_INSTALLED)
    IF (TD_DARWIN)
      message(WARNING "unixodbc is not installed yet, you may install it under macOS by typing: brew install unixodbc")
    ELSE ()
      message(WARNING "odbcinst is not installed yet, you may install it under Ubuntu by typing: sudo apt install odbcinst")
    ENDIF ()
    return ()
  ENDIF ()

  find_program(TD_ISQL_INSTALLED NAMES isql)
  IF (NOT TD_ISQL_INSTALLED)
    IF (TD_DARWIN)
      message(WARNING "unixodbc is not installed yet, you may install it under macOS by typing: brew install unixodbc")
    ELSE ()
      message(WARNING "unixodbc is not installed yet, you may install it under Ubuntu by typing: sudo apt install unixodbc")
    ENDIF ()
    return ()
  ENDIF ()

  find_program(TD_PKG_CONFIG_INSTALLED NAMES pkg-config)
  IF (NOT TD_PKG_CONFIG_INSTALLED)
    IF (TD_DARWIN)
      message(WARNING "pkg-config is not installed yet, you may install it under macOS by typing: brew install pkg-config")
    ELSE ()
      message(WARNING "pkg-config is not installed yet, you may install it under Ubuntu by typing: sudo apt install pkg-config")
    ENDIF ()
    return ()
  ENDIF ()

  EXECUTE_PROCESS(COMMAND pkg-config --variable=includedir odbc ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE ODBC_INCLUDE_DIRECTORY)
  EXECUTE_PROCESS(COMMAND pkg-config --variable=libdir odbc ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE ODBC_LIBRARY_DIRECTORY)
  EXECUTE_PROCESS(COMMAND pkg-config --libs-only-L odbc ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE ODBC_LINK_OPTIONS)

  EXECUTE_PROCESS(COMMAND pkg-config --variable=includedir odbcinst ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE ODBCINST_INCLUDE_DIRECTORY)
  EXECUTE_PROCESS(COMMAND pkg-config --variable=libdir odbcinst ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE ODBCINST_LIBRARY_DIRECTORY)
  EXECUTE_PROCESS(COMMAND pkg-config --libs-only-L odbcinst ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE ODBCINST_LINK_OPTIONS)

  include(CheckSymbolExists)

  set(CMAKE_REQUIRED_LIBRARIES odbc odbcinst)
  set(CMAKE_REQUIRED_INCLUDES ${ODBC_INCLUDE_DIRECTORY} ${ODBCINST_INCLUDE_DIRECTORY})
  set(CMAKE_REQUIRED_LINK_OPTIONS ${ODBC_LINK_OPTIONS} ${ODBCINST_LINK_OPTIONS})

  check_symbol_exists(SQLExecute "sql.h" HAVE_ODBC_DEV)
  IF (NOT HAVE_ODBC_DEV)
    message(WARNING "odbc requirement not satisfied, please install unixodbc-dev. Check detail in ${CMAKE_BINARY_DIR}/CMakeFiles/CMakeError.log")
    return ()
  ENDIF ()

  check_symbol_exists(SQLInstallODBC "odbcinst.h" HAVE_ODBCINST_DEV)
  IF (NOT HAVE_ODBCINST_DEV)
    message(WARNING "odbc requirement not satisfied, check detail in ${CMAKE_BINARY_DIR}/CMakeFiles/CMakeError.log")
    return ()
  ENDIF ()

endmacro()

IF (TD_WINDOWS_64)
  find_package(ODBC)
  if (NOT ODBC_FOUND)
    message(WARNING "you need to install ODBC first")
  else ()
    message(STATUS "ODBC_INCLUDE_DIRS: ${ODBC_INCLUDE_DIRS}")
    message(STATUS "ODBC_LIBRARIES: ${ODBC_LIBRARIES}")
    message(STATUS "ODBC_CONFIG: ${ODBC_CONFIG}")
  endif ()
  find_package(FLEX)
  if(NOT FLEX_FOUND)
    message(WARNING "you need to install flex first\n"
                    "you may go to: https://github.com/lexxmark/winflexbison\n"
                    "or download from: https://github.com/lexxmark/winflexbison/releases")
  else ()
    ADD_SUBDIRECTORY(src)
    ADD_SUBDIRECTORY(tools)
    ADD_SUBDIRECTORY(examples)
  endif()
ELSE ()
  check_odbc_requirement()
  IF (TD_DARWIN)
    SET(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -Wconversion")
    SET(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -Wconversion")
  ENDIF ()
  ADD_SUBDIRECTORY(src)
  ADD_SUBDIRECTORY(tools)
  ADD_SUBDIRECTORY(examples)
ENDIF ()

