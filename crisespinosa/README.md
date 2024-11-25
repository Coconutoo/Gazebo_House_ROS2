# Проект: Сщядфние квартиры с помощью Gazebo

Студент: Эспиноса Василита Кристина Микаела НКНбд-01-22

# Gazebo House ROS2
 Я создалa два мира, во втором мире world1.sdf появляется робот, как вы можете видеть на изображении.

Используемое:
- [VirtualBox 7.1.4](https://www.virtualbox.org/wiki/Downloads)
- [Ubuntu 22.04.5 LTS](https://releases.ubuntu.com/jammy/)
- [Gazebo Classic 11.0.0](https://classic.gazebosim.org/download)
- [Gazebo Ignition 6.16.0](https://gazebosim.org/api/gazebo/6/install.html)
- [ROS2 Humble](https://docs.ros.org/en/humble/Installation.html)

## Этапы выполнения работы

### Создание плана квартиры 

1. Запуск Gazebo с помощью команды 
gazebo --verbose
2. Запуск Edit- Building Editor.
3. С помощью инструментов «Стена», «Дверь» и «Окно» строится 2D-план
4. Сохраняю созданный мир и автоматически создаются файлы  "model.config" и "model.sdf"

### Загрузкa в Gazebo Ignition
1. Создание  файль  'world.sdf' -> Запуск мира в Ignition Gazebo командой
ign gazebo world.sdf 

### Запуск симуляции в turtlebot 3
1. Создание рабочего пространства:
mkdir -p ~/turtlebot3_ws/src
cd ~/turtlebot3_ws/src
wget https://raw.githubusercontent.com/ROBOTIS-GIT/turtlebot3/ros2/turtlebot3.repos
vcs import src < turtlebot3.repos
cd ..
colcon build --symlink-install
echo 'source ~/turtlebot3_ws/install/setup.bash' >> ~/.bashrc

echo 'export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/turtlebot3_ws/src/turtlebot3/turtlebot3_simulations/turtlebot3_gazebo/models' >> ~/.bashrc
echo 'export TURTLEBOT3_MODEL=waffle_pi' >> ~/.bashrc
source ~/.bashrc
### Запуск симуляции в ROS2
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py world:=/home/cristina/turtlebot3_ws/src/turtlebot3/turtlebot3_simulations/turtlebot_gazebo/worlds/world1.sdf

#Открываем новый терминал 

source ~/turtlebot3_ws/install/setup.bash
ros2 run image_tools showimage

#Открываем еще один терминал

~/turtlebot3_ws$ source ~/turtlebot3_ws/install/setup.bash
~/turtlebot3_ws$ ros2 launch turtlebot3_bringup rviz2.launch.py
#RVIZ
1- кнопочка Add
By topic—> на /image_raw/camera

# В новом терминале, чтобы робот двигался
ros2 run turtlebot3_teleop teleop_keyboard
