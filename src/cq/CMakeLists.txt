CMAKE_MINIMUM_REQUIRED(VERSION 3.0...3.20)
PROJECT(TDengine)

INCLUDE_DIRECTORIES(inc)
INCLUDE_DIRECTORIES(${TD_COMMUNITY_DIR}/src/client/inc)
INCLUDE_DIRECTORIES(${TD_COMMUNITY_DIR}/src/query/inc)
AUX_SOURCE_DIRECTORY(${CMAKE_CURRENT_SOURCE_DIR}/src SRC)

ADD_LIBRARY(tcq ${SRC})
IF (TD_SOMODE_STATIC)
  TARGET_LINK_LIBRARIES(tcq tutil common taos_static)
ELSE ()
  TARGET_LINK_LIBRARIES(tcq tutil common taos)
ENDIF ()
ADD_SUBDIRECTORY(test)
