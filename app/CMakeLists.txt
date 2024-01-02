# CMAKE_PROJECT_NAME will be the root project
project(${CMAKE_PROJECT_NAME}_app)

add_executable(${PROJECT_NAME})

# change app name to be that of the root project
set_target_properties(${PROJECT_NAME} PROPERTIES
    OUTPUT_NAME ${CMAKE_PROJECT_NAME}
)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

target_sources(${PROJECT_NAME} PRIVATE
    src/main.cpp
)

target_include_directories(${PROJECT_NAME} PRIVATE
    inc/
    aruco/
)

find_package(fmt REQUIRED)

set(CMAKE_CXX_FLAGS_RELEASE "-O3")

target_link_libraries(${PROJECT_NAME} PRIVATE
    ${OpenCV_LIBS}
    fmt::fmt
)
