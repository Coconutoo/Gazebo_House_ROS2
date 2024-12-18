# Этапы выполнения работы.

## Создание квартиры
1. Сначала я запустила gazebo.
2. Потом зашла в режим building_editor и начертила 2д макет квартиры.
3. Вставила элементы Wall, Window и Door.
4. Сохранила модель в папке building_editor_models

## Загрузка квартиры в Ignition Gazebo
1. Создала в папке building_editor_models файл world.sdf, который позволяет загрузить квартиру в мир Ignition Gazebo, используя модель из файла model.sdf
2. Загрузила мир командой 
ign gazebo world.sdf 
3. В симуляции загрузила предметы мебели, пол и свет.
4. Сохранила мир через "Save world as", файл с раширением sdf (лучше выбрать тот же самый файл world.sdf), поставил "Expand include tags" и "Save Fuel model version".

## Запуск симуляции с turtlebot 3
1. Создала рабочее пространство для TurtleBot 3:
<pre><code>mkdir -p ~/turtlebot3_ws/src</code></pre>
<pre><code>cd ~/turtlebot3_ws/src</code></pre>
<pre><code>git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git</code></pre>
2. Собрала рабочее пространство:
<pre><code>cd ~/turtlebot3_ws && colcon build --symlink-install</code></pre>
3. Запустила симуляцию TurtleBot 3:
<pre><code>ros2 launch turtlebot3_gazebo myworld.launch.py</code></pre>
