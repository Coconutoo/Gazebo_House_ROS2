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

### Запуск симуляции в turtlebot 4
1. Создание рабочего пространства:
mkdir -p ~/project/vlbarsegyan/turtlebot4_ws/src
cd ~/project/vlbarsegyan/turtlebot4_ws/src
git clone https://github.com/turtlebot/turtlebot4.git
cd ..
colcon build --symlink-install

### Запуск симуляции в ROS2
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py world:=/home/cristina/turtlebot3_ws/src/turtlebot3/turtlebot3_simulations/turtlebot_gazebo/worlds/world1.sdf

