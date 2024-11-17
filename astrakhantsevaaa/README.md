Струкрута проекта должна соответствовать:
```bash
ros2_ws/
├── src/
│   ├── turtlebot3_simulations/
│   │   ├── turtlebot3_gazebo/
│   │   │   ├── launch/
│   │   │   │   ├── world_my1.launch.py
│   │   │   ├── worlds/
│   │   │   │   ├── world_my1.sdf
│   │   │   ├── models/
│   │   │   ├── CMakeLists.txt
│   │   │   ├── package.xml
│   ├── ... другие пакеты ...

```
Поместите файл install_project.sh в корень рабочего пространства (ros2_ws).
Дайте скрипту права на выполнение:
```
chmod +x install_project.sh
```
Далее нужно склонировать репозиторий
```
   git clone git@github.com:AI-group-72/Gazebo_House_ROS2.git ~/ros2_ws/src
```
Перейдите в рабочее пространство:
```
cd ~/ros2_ws
```
Запустите скрипт установки. Выполните эту команду только один раз после добавления файла `install_project.sh`.

```
./install_project.sh
```
Активируйте рабочее пространство (выполните эту команду в каждом новом окне терминала перед запуском ROS-команд)
```
source ~/ros2_ws/install/setup.bash
```
**Запуск симуляции**
Запустите мир:
```
ros2 launch turtlebot3_gazebo world_my1.launch.py
```
В другом окне терминала запускаем команду для управления роботом:
```
ros2 run turtlebot3_teleop teleop_keyboard

```
Для отображения в RViz2:
```
ros2 launch turtlebot3_bringup rviz2.launch.py
```
В RViz2 добавьте дисплей типа `Image` и укажите топик `/camera/image_raw` для отображения.



