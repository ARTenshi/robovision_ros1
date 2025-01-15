cmake_minimum_required(VERSION 2.8.3)
project(introvision_processing)

find_package(catkin REQUIRED COMPONENTS cv_bridge image_transport message_generation roscpp sensor_msgs std_msgs)
find_package(OpenCV REQUIRED)

catkin_package()

include_directories(include ${catkin_INCLUDE_DIRS} ${OpenCV_INCLUDE_DIRS})

# add the publisher example
add_executable(my_processing src/my_processing.cpp)
add_dependencies(my_processing ${catkin_EXPORTED_TARGETS} ${${PROJECT_NAME}_EXPORTED_TARGETS})
target_link_libraries(my_processing ${catkin_LIBRARIES} ${OpenCV_LIBRARIES})

# Mark executables and/or libraries for installation
install(TARGETS my_processing
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

