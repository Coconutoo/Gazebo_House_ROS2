import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan
import csv
import cv2
from cv_bridge import CvBridge
import time

class ImageLidarSaver(Node):
    def __init__(self):
        super().__init__('image_lidar_saver')

        # Подписка на топик камеры
        self.image_subscription = self.create_subscription(
            Image,
            '/camera/image_raw',  # Замените на ваш топик, если он другой
            self.image_callback,
            10)

        # Подписка на топик лидара
        self.lidar_subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10)

        # Инициализация конвертера для изображений
        self.bridge = CvBridge()

        # Файл для сохранения данных
        self.csv_file = open('image_lidar_data_rgb.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp', 'Lidar Data', 'Image RGB'])

        # Переменные для хранения данных
        self.lidar_data = []  # Хранит данные лидара
        self.image_rgb = None  # Хранит текущее изображение в формате RGB

    def image_callback(self, msg):
        """Обработчик изображений с камеры."""
        try:
            # Конвертация изображения ROS -> OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

            # Преобразуем изображение в RGB
            cv_image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

            # Сохраняем изображение как список RGB-значений
            self.image_rgb = cv_image_rgb.tolist()

            # Сохраняем данные в CSV, если есть данные лидара
            if self.image_rgb and self.lidar_data:
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
        """Сохранение данных изображения и лидара в CSV."""
        try:
            # Генерация метки времени
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            # Запись данных в CSV
            self.csv_writer.writerow([timestamp, self.lidar_data, self.image_rgb])
            self.get_logger().info(f'Saved data at {timestamp}')
        except Exception as e:
            self.get_logger().error(f'Error saving data: {e}')

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

