## **Инструкция по установке и запуску**

### **1. Клонирование репозитория**
```bash
git clone git@github.com:AI-group-72/Gazebo_House_ROS2.git ~/ros2_ws/src
```

### **2. Создание структуры проекта**
Перенесите файлы в рабочее пространство таким образом, чтобы структура соответствовала:
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

---

### **3. Установка зависимостей**
После того как файлы будут размещены в нужных директориях, выполните следующий шаг.

1. Поместите файл `install_project.sh` в корень рабочего пространства (`ros2_ws`).
2. Дайте файлу права на выполнение:

   ```bash
   chmod +x install_project.sh
   ```
3. Запустите скрипт установки:

   ```bash
   ./install_project.sh
   ```

---

### **4. Активация рабочего пространства**
Перед запуском ROS-команд активируйте рабочее пространство (эту команду нужно выполнять в каждом новом окне терминала):
```bash
source ~/ros2_ws/install/setup.bash
```

---

## **Запуск симуляции**

1. Запустите мир:
   ```bash
   ros2 launch turtlebot3_gazebo world_my1.launch.py
   ```

2. Для управления роботом в другом окне терминала:
   ```bash
   ros2 run turtlebot3_teleop teleop_keyboard
   ```

3. Для визуализации в RViz2:
   ```bash
   ros2 launch turtlebot3_bringup rviz2.launch.py
   ```

4. В RViz2 добавьте дисплей типа `Image` и укажите топик `/camera/image_raw` для отображения.


