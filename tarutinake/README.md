
# Gazebo House ROS2

Используемое ПО:
- [Ubuntu 22.04.5 LTS (Jammy Jeelyfish)](https://releases.ubuntu.com/jammy/)
- [Gazebo Classic 11.0.0](https://classic.gazebosim.org/download)
- [ROS2 Humble](https://docs.ros.org/en/humble/Installation.html)
- [Gazebo Ignition 6.16.0](https://gazebosim.org/api/gazebo/6/install.html)

## Запуск симуляции с turtlebot 4
1. Создание рабочего пространства:
```
mkdir -p ~/turtlebot4_ws/src
cd ~/turtlebot4_ws/src
git clone https://github.com/turtlebot/turtlebot4.git
cd ~/turtlebot4_ws
colcon build --symlink-install
```
2. Запуск симуляции в ROS2
```
ros2 launch turtlebot4_ignition_bringup turtlebot4_ignition.launch.py world:=world x:=2.5 y:=4.5
```
