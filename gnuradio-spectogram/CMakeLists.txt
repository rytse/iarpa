# Specify the minimum version for CMake

cmake_minimum_required(VERSION 3.8)

# Project's name

project(gnuradio-spectogram)
# Set the output folder where your program will be created
set(CMAKE_BINARY_DIR ${CMAKE_SOURCE_DIR}/bin)
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR})
set(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR})
set(PROJECT_SOURCE_DIR ${CMAKE_SOURCE_DIR}/src)

# include(GrVersion) #setup version info
# include(GrPlatform) #define LIB_SUFFIX
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(GR_REQUIRED_COMPONENTS RUNTIME BLOCKS FFT)
find_package(Gnuradio "3.8.0" REQUIRED)
find_package(Boost "1.65" REQUIRED COMPONENTS filesystem system)

if(Gnuradio_FOUND)
    message(STATUS "Gnuradio found")


    
    pkg_check_modules(GNURADIO_PKG REQUIRED IMPORTED_TARGET gnuradio-runtime gnuradio-blocks gnuradio-fft)
    include_directories(${Boost_INCLUDE_DIRS}
        ${GNURADIO_PKG_INCLUDE_DIRS})
    
    link_directories(${GNURADIO_PKG_LIBRARY_DIRS})
    # get_cmake_property(_variableNames VARIABLES)
    # list (SORT _variableNames)
    # foreach (_variableName ${_variableNames})
    #     message(STATUS "${_variableName}=${${_variableName}}")
    # endforeach()
    add_executable(${PROJECT_NAME} ${PROJECT_SOURCE_DIR}/main.cpp)
    message(STATUS "Found Gnuradio libraries for project: ${PROJECT_NAME}, dir: ${Gnuradio_DIR}, ${GNURADIO_PKG_LIBRARIES}, ,  ${GNURADIO_PKG_CFLAGS_OTHER}")

    # message(STATUS ${PkgConfig::GNURADIO_PKG})
    target_link_libraries(${PROJECT_NAME}
            ${Boost_LIBRARIES}
            # PkgConfig::GNURADIO_PKG)
            ${GNURADIO_PKG_LIBRARIES})
else()
    message(WARNING, "Gnuradio not found")
endif()

# # The following folder will be included
# include_directories(
#     ${PROJECT_SOURCE_DIR}
#     ${GNU_RADIO_PATH}/include
# )

# link_directories(
#     # ${Boost_LIBRARY_DIRS}
#     ${GNU_RADIO_PATH}/lib
# )


# target_link_libraries(${PROJECT_NAME} gnuradio-runtime gnuradio-fft gnuradio-blocks)