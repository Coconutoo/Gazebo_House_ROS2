#!/bin/bash
# Скрипт для установки и настройки проекта ROS 2

if [ -z "$ROS_DISTRO" ]; then
  echo "ROS 2 не найден. Убедитесь, что установлен ROS 2 Humble."
  exit 1
fi

echo "Установка необходимых зависимостей..."
sudo apt update
sudo apt install -y python3-colcon-common-extensions ros-humble-gazebo-ros-pkgs

echo "Сборка рабочего пространства..."
cd ~/ros2_ws
colcon build --symlink-install

echo "Готово! Используйте 'source ~/ros2_ws/install/setup.bash' для активации пространства."

