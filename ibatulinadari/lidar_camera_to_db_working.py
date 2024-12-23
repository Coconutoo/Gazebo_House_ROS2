import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan
import psycopg2
from psycopg2 import sql, extras
from cv_bridge import CvBridge
import cv2
import time
import numpy as np

class ImageLidarSaver(Node):
    def __init__(self):
        super().__init__('image_lidar_saver')

        # Логируем запуск узла
        self.get_logger().info("Node 'image_lidar_saver' has started")

        # Подключение к базе данных
        try:
            self.db_connection = psycopg2.connect(
                database="lidar_camera_data",
                user="lidar_user",
                password="secure_password",
                host="localhost",
                port="5432"
            )
            self.get_logger().info("Connected to the database successfully")
        except Exception as e:
            self.get_logger().error(f"Failed to connect to the database: {e}")
            return

        # Создание подписок
        self.image_subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)
        self.lidar_subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10)

        # Инициализация переменных
        self.bridge = CvBridge()
        self.lidar_data = []  # Данные лидара
        self.image_rgb = None  # Данные изображения

    def image_callback(self, msg):
        """Обработчик изображений с камеры."""
        self.get_logger().info("Received image data")
        try:
            # Преобразуем изображение в OpenCV формат
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
            # Конвертируем в RGB
            self.image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB).tolist()
            self.get_logger().info("Processed image data")
            self.save_data()
        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")

    def lidar_callback(self, msg):
        """Обработчик данных с лидара."""
        self.get_logger().info("Received lidar data")
        try:
            self.lidar_data = []
            angle = msg.angle_min
            for r in msg.ranges:
                angle_deg = angle * 180.0 / 3.14159265359
                if -30 <= angle_deg <= 30:
                    self.lidar_data.append(r)
                angle += msg.angle_increment
            self.get_logger().info(f"Processed lidar data: {len(self.lidar_data)} points")
        except Exception as e:
            self.get_logger().error(f"Error processing lidar: {e}")

    def save_data(self):
        """Сохранение данных в базу данных."""
        if self.lidar_data and self.image_rgb:
            try:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                # Преобразуем изображение в байты
                if self.image_rgb is not None:
                    image_array = np.array(self.image_rgb, dtype=np.uint8)
                    image_bytes = cv2.imencode('.jpg', cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR))[1].tobytes()
                else:
                    raise ValueError("Image data is not valid")

                # Преобразуем список данных лидара в JSON
                lidar_array = psycopg2.extras.Json(self.lidar_data)

                with self.db_connection.cursor() as cursor:
                    cursor.execute(
                        sql.SQL("INSERT INTO lidar_camera_data (timestamp, lidar_data, image_rgb) VALUES (%s, %s, %s)"),
                        (timestamp, lidar_array, image_bytes)
                    )
                    self.db_connection.commit()
                self.get_logger().info(f"Saved data to database at {timestamp}")
            except Exception as e:
                self.get_logger().error(f"Error saving to database: {e}")

    def destroy_node(self):
        """Закрытие подключения при завершении узла."""
        self.db_connection.close()
        self.get_logger().info("Database connection closed")
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ImageLidarSaver()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Node interrupted, shutting down")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

