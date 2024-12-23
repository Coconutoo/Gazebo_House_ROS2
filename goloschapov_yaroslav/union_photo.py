import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan
import cv2
from cv_bridge import CvBridge
import csv
import os
import time
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class LidarCameraSaver(Node):
    def __init__(self):
        super().__init__('lidar_camera_saver')  # Указание имени узла


        # Подписка на топик камеры
        self.image_subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            20)

        # Подписка на топик лидара
        self.lidar_subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            20)

        # Инициализация конвертера для изображений
        self.bridge = CvBridge()

        # Настройка директорий
        self.image_dir = 'images'  # Папка для сохранения изображений
        os.makedirs(self.image_dir, exist_ok=True)

        # Настройка CSV-файла
        self.csv_file = open('lidar_camera_data_images.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp', 'Image Path', 'Lidar Data', 'Detected Objects'])

        # Переменные для хранения данных
        self.lidar_data = []  # Данные лидара
        self.image_path = None  # Путь к текущему изображению

        # Загрузка модели YOLOv5x
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5x')

        # Инициализация модели генерации текста
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.model_gpt2 = GPT2LMHeadModel.from_pretrained('gpt2')

    def image_callback(self, msg):
        """Обработчик изображений с камеры."""
        try:
            # Конвертация изображения ROS -> OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

            # Формируем имя файла для изображения
            timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
            image_filename = f'{self.image_dir}/image_{timestamp}.png'

            # Сохраняем изображение в файл
            cv2.imwrite(image_filename, cv_image)

            # Сохраняем путь к изображению
            self.image_path = image_filename

            # Распознавание объектов
            results = self.model(cv_image)
            detected_objects = results.pandas().xyxy[0].to_json(orient="records")

            # Генерация описания на естественном языке
            input_text = f"В комнате находятся: {detected_objects}"
            input_ids = self.tokenizer.encode(input_text, return_tensors='pt')
            output = self.model_gpt2.generate(input_ids, max_new_tokens=50)
            description = self.tokenizer.decode(output[0], skip_special_tokens=True)
            self.get_logger().info(description)

            # Сохраняем данные (если есть лидарные данные)
            self.save_data(detected_objects, description)

        except Exception as e:
            self.get_logger().error(f'Error saving image: {e}')

    def lidar_callback(self, msg):
        """Обработчик данных с лидара."""
        self.lidar_data = []  # Сохраняем только свежие данные

        # Фильтруем данные лидара: 
        angle = msg.angle_min
        for r in msg.ranges:
            angle_deg = angle * 180.0 / 3.14159265359
            if -30 <= angle_deg <= 30:  # Углы перед роботом
                self.lidar_data.append(r)
            angle += msg.angle_increment

    def save_data(self, detected_objects, description):
        """Сохраняет данные с камеры и лидара в CSV."""
        if self.image_path and self.lidar_data:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.csv_writer.writerow([timestamp, self.image_path, self.lidar_data, description])
            self.get_logger().info(f'Saved data: {timestamp}, Image: {self.image_path}, Objects: {description}')

def destroy_node(self):
        """Закрытие файла при завершении узла."""
        self.csv_file.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = LidarCameraSaver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
