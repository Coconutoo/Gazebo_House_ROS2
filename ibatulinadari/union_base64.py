import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan
import csv
import cv2
from cv_bridge import CvBridge
import base64
import time


class ImageLidarSaver(Node):
    def __init__(self):
        super().__init__('image_lidar_saver')

        # Подписка на топик камеры
        self.image_subscription = self.create_subscription(
            Image,
            '/camera/image_raw',  # Замените на ваш топик, если он другой
            self.image_callback,
            10
        )

        # Подписка на топик лидара
        self.lidar_subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10
        )

        # Инициализация конвертера для изображений
        self.bridge = CvBridge()

        # Файл для сохранения данных
        self.csv_file = open('image_lidar_data_base64.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp', 'Lidar Data', 'Image (Base64)'])

        # Переменные для хранения данных
        self.lidar_data = []  # Хранит данные лидара
        self.image_encoded = None  # Хранит текущее изображение в формате Base64

    def image_callback(self, msg):
        """Обработчик изображений с камеры."""
        try:
            # Конвертация изображения ROS -> OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

            # Кодируем изображение в Base64
            _, buffer = cv2.imencode('.png', cv_image)
            self.image_encoded = base64.b64encode(buffer).decode('utf-8')

            # После получения нового изображения записываем данные
            self.save_data()

        except Exception as e:
            self.get_logger().error(f'Error processing image: {e}')

    def lidar_callback(self, msg):
        """Обработчик данных с лидара."""
        self.lidar_data = []  # Обновляем данные лидара

        # Сохраняем только данные перед роботом (угол от -30° до +30°)
        angle = msg.angle_min
        for r in msg.ranges:
            # Конвертируем угол в градусы
            angle_deg = angle * 180.0 / 3.14159265359
            if -30 <= angle_deg <= 30:  # Фильтруем только перед роботом
                self.lidar_data.append(r)
            angle += msg.angle_increment

    def save_data(self):
        """Сохраняет данные с камеры и лидара в CSV."""
        if self.image_encoded and self.lidar_data:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.csv_writer.writerow([timestamp, self.lidar_data, self.image_encoded])
            self.get_logger().info(f'Saved data at {timestamp}')

    def destroy_node(self):
        """Закрытие файла при завершении узла."""
        self.csv_file.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ImageLidarSaver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

