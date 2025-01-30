import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan
from cv_bridge import CvBridge
import numpy as np
import sqlite3
import time
import cv2
import os

class SaveVideoWithLidar(Node):
    def __init__(self):
        super().__init__('save_video_with_lidar')
        
        # Подключение к базе данных SQLite
        self.conn = sqlite3.connect('robot_data.db')
        self.cursor = self.conn.cursor()
        
        # Сообщение о пути к базе данных
        self.get_logger().info(f"База данных находится по пути:{os.path.abspath('robot_data.db')}")
        self.create_table()

        # Подписка на топики камеры и лидар
        self.bridge = CvBridge()
        self.image_sub = self.create_subscription(
            Image,  # Изменено с CompressedImage на Image
            '/camera/image_raw',  # Топик необработанных изображений
            self.image_callback,
            10
        )

        self.lidar_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10
        )

        self.lidar_data = None  # Переменная для хранения данных лидара
        self.get_logger().info("Подписки активированы")

    def create_table(self):
        """Создание таблицы в базе данных, если её нет"""
        self.get_logger().info("Создание таблицы в базе данных")
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS robot_data (
                timestamp TEXT,
                image BLOB,
                lidar_coordinates BLOB
            )
        ''')
        self.conn.commit()

    def lidar_callback(self, msg):
        """Обработка данных лидара и конвертация в координаты (x, y)"""
        angle = msg.angle_min
        coordinates = []

        for distance in msg.ranges:
            if msg.range_min <= distance <= msg.range_max:
                x = distance * np.cos(angle)
                y = distance * np.sin(angle)
                coordinates.append((x, y))
            angle += msg.angle_increment

        self.lidar_data = np.array(coordinates, dtype=np.float32)

    def image_callback(self, msg):
        """Обработка изображения с камеры и сохранение вместе с данными лидара"""
        if self.lidar_data is None:
            self.get_logger().info('Ожидание данных лидара...')
            return

        try:
            # Конвертация необработанного изображения в формат OpenCV
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Отображение изображения для отладки (опционально)
            cv2.imshow("Захваченное изображение", frame)
            cv2.waitKey(1)  # Короткое отображение изображения

            # Сжатие изображения в формате JPEG для сохранения в базу данных
            success, buffer = cv2.imencode('.jpg', frame)
            if not success:
                self.get_logger().error('Ошибка сжатия изображения.')
                return

            frame_bytes = buffer.tobytes()
            lidar_bytes = self.lidar_data.tobytes()

            # Отладка: Проверка размеров перед сохранением
            self.get_logger().info(f'Размер сжатого изображения (байты): {len(frame_bytes)}')
            self.get_logger().info(f'Размер данных лидара (байты): {len(lidar_bytes)}')

            # Получение текущего временного штампа
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # Вставка данных в базу данных
            self.cursor.execute(
                'INSERT INTO robot_data (timestamp, image, lidar_coordinates) VALUES (?, ?, ?)',
                (timestamp, frame_bytes, lidar_bytes)
            )
            self.conn.commit()

            self.get_logger().info(f'Данные сохранены в базе данных: {timestamp}')

        except Exception as e:
            self.get_logger().error(f'Ошибка в image_callback: {e}')

    def destroy_node(self):
        """Закрытие соединения с базой данных при завершении"""
        self.conn.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SaveVideoWithLidar()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
