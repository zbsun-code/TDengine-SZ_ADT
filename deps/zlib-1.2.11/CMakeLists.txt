CMAKE_MINIMUM_REQUIRED(VERSION 3.0...3.20)
PROJECT(TDengine)

IF (TD_WINDOWS)
  SET(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} /WX-")
  SET(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} /WX-")
ENDIF()

INCLUDE_DIRECTORIES(inc)
AUX_SOURCE_DIRECTORY(src SRC)
ADD_LIBRARY(z ${SRC})
