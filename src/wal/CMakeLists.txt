CMAKE_MINIMUM_REQUIRED(VERSION 3.0...3.20)
PROJECT(TDengine)

ADD_DEFINITIONS(-DWAL_CHECKSUM_WHOLE)

INCLUDE_DIRECTORIES(inc)
AUX_SOURCE_DIRECTORY(${CMAKE_CURRENT_SOURCE_DIR}/src SRC)

ADD_LIBRARY(twal ${SRC})
TARGET_LINK_LIBRARIES(twal tutil common)
ADD_SUBDIRECTORY(test)
