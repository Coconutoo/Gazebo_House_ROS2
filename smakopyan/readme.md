
/turtlebot3_ws$ source install/local_setup.bash

/turtlebot3_ws$ export TURTLEBOT3_MODEL=waffle

/turtlebot3_ws$ ros2 launch turtlebot3_gazebo world.launch.py


в другом окне

/turtlebot3_ws$ source ~/turtlebot3_ws/install/setup.bash

/turtlebot3_ws$ ros2 run turtlebot3_teleop teleop_keyboard
