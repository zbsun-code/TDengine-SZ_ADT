CMAKE_MINIMUM_REQUIRED(VERSION 3.0...3.20)
PROJECT(TDengine)

FIND_PATH(HEADER_GTEST_INCLUDE_DIR gtest.h /usr/include/gtest /usr/local/include/gtest)
FIND_LIBRARY(LIB_GTEST_STATIC_DIR libgtest.a /usr/lib/ /usr/local/lib /usr/lib64)
FIND_LIBRARY(LIB_GTEST_SHARED_DIR libgtest.so /usr/lib/ /usr/local/lib /usr/lib64)

IF (HEADER_GTEST_INCLUDE_DIR AND (LIB_GTEST_STATIC_DIR OR LIB_GTEST_SHARED_DIR))
    MESSAGE(STATUS "gTest library found, build unit test")

    INCLUDE_DIRECTORIES(${HEADER_GTEST_INCLUDE_DIR})
    AUX_SOURCE_DIRECTORY(${CMAKE_CURRENT_SOURCE_DIR} SOURCE_LIST)

    LIST(REMOVE_ITEM SOURCE_LIST ${CMAKE_CURRENT_SOURCE_DIR}/trefTest.c)
    ADD_EXECUTABLE(utilTest ${SOURCE_LIST})
    TARGET_LINK_LIBRARIES(utilTest tutil common os gtest pthread gcov)

    LIST(APPEND BIN_SRC ${CMAKE_CURRENT_SOURCE_DIR}/trefTest.c)
    ADD_EXECUTABLE(trefTest ${BIN_SRC})
    TARGET_LINK_LIBRARIES(trefTest common tutil)

ENDIF()

#IF (TD_LINUX)
#    ADD_EXECUTABLE(trefTest ./trefTest.c)
#    TARGET_LINK_LIBRARIES(trefTest tutil common)
#ENDIF ()

INCLUDE_DIRECTORIES(${TD_COMMUNITY_DIR}/src/util/inc)


