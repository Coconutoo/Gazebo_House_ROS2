#!/bin/bash
# Скрипт для установки и настройки проекта ROS 2

echo "Проверка установки ROS 2..."
if [ -z "$ROS_DISTRO" ]; then
  echo "ROS 2 не найден. Устанавливаем ROS 2 Humble..."
  
  # Установка ROS 2 Humble
  sudo apt update
  sudo apt install -y curl gnupg lsb-release
  curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo tee /usr/share/keyrings/ros-archive-keyring.gpg > /dev/null
  echo "deb [signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2-latest.list > /dev/null
  sudo apt update
  sudo apt install -y ros-humble-desktop

  # Настройка окружения
  echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
  source ~/.bashrc
else
  echo "ROS 2 уже установлен. Текущая дистрибуция: $ROS_DISTRO"
fi

echo "Установка необходимых зависимостей..."
sudo apt update
sudo apt install -y python3-colcon-common-extensions ros-humble-gazebo-ros-pkgs

# Установка Turtlebot3 (без запроса)
echo "Устанавливаем Turtlebot3..."
sudo apt install -y ros-humble-turtlebot3* 
echo "export TURTLEBOT3_MODEL=waffle" >> ~/.bashrc
source ~/.bashrc

echo "Установка завершена. Теперь переместите файлы проекта в нужные директории."

