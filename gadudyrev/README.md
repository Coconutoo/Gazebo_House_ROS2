# Создание симуляции TurtleBot4 в Gazebo

## Описание работы

В данной работе мы создадим мир при помощи инструмента Gazebo и проведем в нем симуляцию TurtleBot4.

## Используемая среда

Перед началом необходимо настроить рабочую среду на вашем компьютере. Лично я использовал виртуальную машину Ubuntu 22.04.5 LTS (Jammy Jellyfisf) в VirtualBox, 
на нее я поставил Ros2-Humble, Gazebo Classic и Gazebo Ignition. Я не буду останавливаться на том, как поставить виртуальную машину и установить остальное ПО, 
потому что тема этого мануала про работу с Gazebo и ROS2, но вы можете воспользоваться ссылками ниже для их установки:

* [Ubuntu 22.04.5 LTS (Jammy Jellyfish)](https://releases.ubuntu.com/jammy/)
* [ROS2-Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)
* [Gazebo Ignition 6.16.0](https://gazebosim.org/api/gazebo/6/install.html)
* [Gazebo 11.10.2](https://classic.gazebosim.org/download)

## Подготовка рабочего пространства ROS2

1. Для корректной работы ROS2 необходимо создать особое рабочее пространство, для ROS2-Humble необходимо будет воспользоваться инструментом colcon,
   чтобы его установить воспользуйтесь следующей командой:
   
   `sudo apt install python3-colcon-common-extensions`

2. Далее необходимо изменить файл ~/.bashrc, чтобы colcon стал доступным после каждого перезапуска терминала.

   `echo 'source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash' >> ~/.bashrc`

   перезапускаем терминал и продолжаем работу.

4. Теперь перейдем к созданию рабочего пространства ROS2, создадим директорию, внутри которой будет находиться это рабочее пространство:
   
   `mkdir ~/demo_ws`

5. Также создадим папку, которая будет хранить все пакеты ROS2:

   `mkdir ~/demo_ws/src`

6. Теперь инициализируем рабочее пространство, используя colcon:

   `cd ~/demo_ws`
   
   `colcon build --symlink-install`

   В итоге в директории ~/demo_ws должны находиться папки build, install, log и ранее созданная src.

7. Чтобы мы могли обращаться к пакетам ROS2 отовсюду, изменим файл ~/.bashrc

   `echo 'source ~/demo_ws/install/setup.bash' >> ~/.bashrc`

Теперь наше рабочее пространство готово, вернемся к нему позже.

## Создание модели здания с помощью Building Editor в Gazebo

Если вы уже установили Gazebo Classic, то выполняйте действия ниже, если нет, то перейдите по ссылке для скачивания, которая находится выше.

1. Итак, открываем динамический симулятор Gazebo, введя в терминал:

   `gazebo`

   откроется приложение, как на картинке ниже.

![Gazebo Classic](./images/1.png)

2. Далее либо используя комбинацию клавишь Ctrl+B, либо через меню сверху открываем Building Editor.

![Building Editor](./images/2.png)
   
   
   
