CMAKE_MINIMUM_REQUIRED(VERSION 3.0...3.20)
PROJECT(TDengine)

LIST(APPEND CQTEST_SRC ./cqtest.c)
ADD_EXECUTABLE(cqtest ${CQTEST_SRC})
TARGET_LINK_LIBRARIES(cqtest tcq taos_static)
