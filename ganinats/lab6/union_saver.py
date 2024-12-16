import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan
import cv2
from cv_bridge import CvBridge
import csv
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
        self.csv_file = open('image_lidar_data.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp', 'Image File', 'Lidar Data'])

        # Переменные для хранения данных
        self.lidar_data = []  # Хранит данные лидара
        self.last_save_time = time.time()  # Время последнего сохранения
        self.image_frame_count = 0  # Счётчик кадров

    def image_callback(self, msg):
        """Обработчик изображений с камеры."""
        try:
            # Конвертация изображения ROS -> OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
            
            # Сохраняем изображение
            image_filename = f'frame_{self.image_frame_count}.png'
            cv2.imwrite(image_filename, cv_image)
            self.get_logger().info(f'Saved {image_filename}')

            # Сохраняем кадр и данные лидара, если прошло >= 15 секунд
            current_time = time.time()
            if current_time - self.last_save_time >= 15 and self.lidar_data:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                self.csv_writer.writerow([timestamp, image_filename, self.lidar_data])
                self.get_logger().info(f'Saved image and lidar data at {timestamp}')
                self.last_save_time = current_time

            # Обновляем счётчик кадров
            self.image_frame_count += 1

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

