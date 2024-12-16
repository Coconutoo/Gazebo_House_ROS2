import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class ImageSaver(Node):
    def __init__(self):
        super().__init__('image_saver')
        # Подписываемся на топик камеры
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',  # Замените на ваш топик, если он другой
            self.listener_callback,
            10)
        self.bridge = CvBridge()  # Конвертер ROS-изображений в OpenCV
        self.frame_count = 0  # Счётчик кадров

    def listener_callback(self, msg):
        try:
            # Конвертируем ROS Image в формат OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
            # Сохраняем кадр в файл
            filename = f'frame_{self.frame_count}.png'
            cv2.imwrite(filename, cv_image)
            self.get_logger().info(f'Saved {filename}')
            self.frame_count += 1
        except Exception as e:
            self.get_logger().error(f'Error saving image: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = ImageSaver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

