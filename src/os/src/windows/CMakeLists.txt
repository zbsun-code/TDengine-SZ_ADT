CMAKE_MINIMUM_REQUIRED(VERSION 3.0...3.20)
PROJECT(TDengine)

AUX_SOURCE_DIRECTORY(. SRC)
ADD_LIBRARY(oswindows ${SRC})

TARGET_LINK_LIBRARIES(oswindows winmm IPHLPAPI ws2_32 MsvcLibXw)