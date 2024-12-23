import rclpy # для работы с рос2
from rclpy.node import Node # для создания узлов рос
from sensor_msgs.msg import Image, LaserScan # для обработки данных с камеры и лидара
import psycopg2 # для работы с постгрескул
from psycopg2 import sql # для скл запросов
from cv_bridge import CvBridge # для преобразования между форматами
import cv2 # для обработки изображений
import time # время

class ImageLidarSaver(Node):
    def __init__(self):
        super().__init__('image_lidar_saver') #  инициализация узла

        # Логируем запуск узла(узел запущен)
        self.get_logger().info("Node 'image_lidar_saver' has started")

        # Подключение к базе данных
        try:
            self.db_connection = psycopg2.connect(
                database="lidar_camers_data",
                user="lidar_user",
                password="12345",
                host="localhost",
                port="5432"
            )
            self.get_logger().info("Connected to the database successfully")
        except Exception as e: # если подключение не удалось
            self.get_logger().error(f"Failed to connect to the database: {e}")
            return

        # Создание подписок на изображения(данные с камеры)
        self.image_subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)
        #  Создание подписок на данные с лидара
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
        self.get_logger().info("Received image data") # сообощение, что данные изображения получены
        try: # обработка изображений(рос-опенСВ, конвертация изобр. из БГР в РГБ)
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
            self.image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB).tolist()
            self.get_logger().info("Processed image data")
            self.save_data()
        except Exception as e: # ошибка при обработке изображения
            self.get_logger().error(f"Error processing image: {e}")

    def lidar_callback(self, msg): # обработка данных с лидара
        """Обработчик данных с лидара."""
        self.get_logger().info("Received lidar data") # данные с лидара полоучены
        try: # обработка данных лидара
# перебор расстояний, преобразование углов в градусы и фильтрация по углу
            self.lidar_data = []
            angle = msg.angle_min
            for r in msg.ranges:
                angle_deg = angle * 180.0 / 3.14159265359
                if -30 <= angle_deg <= 30:
                    self.lidar_data.append(r)
                angle += msg.angle_increment
            self.get_logger().info(f"Processed lidar data: {len(self.lidar_data)} points")
        except Exception as e: # ошибка при обработке лидарак
            self.get_logger().error(f"Error processing lidar: {e}")

    def save_data(self): # метод для сохранения данных в базу
        """Сохранение данных в базу данных."""
        if self.lidar_data and self.image_rgb: # проверка наличия данных
# получение времени, открытие скл, выполнение запроса с передачей временной метки, данных лидара и изображения в формате строки
            try:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                with self.db_connection.cursor() as cursor:
                    cursor.execute(
                        sql.SQL("INSERT INTO lidar_camera_data (timestamp, lidar_data, image_rgb) VALUES (%s, %s, %s)"),
                        (timestamp, str(self.lidar_data), str(self.image_rgb))
                    )
                    self.db_connection.commit()
                self.get_logger().info(f"Saved data to database at {timestamp}")
            except Exception as e: # ошибка при сохранении в базу данных
                self.get_logger().error(f"Error saving to database: {e}")

    def destroy_node(self): # метод для завершения работы узла
        """Закрытие подключения при завершении узла."""
        self.db_connection.close()
        self.get_logger().info("Database connection closed")
        super().destroy_node()

def main(args=None): # инициализирует систму рос2
    rclpy.init(args=args)
    node = ImageLidarSaver()
    try: # запуск узла
        rclpy.spin(node)
    except KeyboardInterrupt: # обработка прерывания
        node.get_logger().info("Node interrupted, shutting down")
    finally: # очистка ресурсов
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

