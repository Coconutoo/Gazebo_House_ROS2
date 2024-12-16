import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan
from cv_bridge import CvBridge
import cv2
import math
import numpy as np
from datetime import datetime
from sklearn.cluster import DBSCAN
import csv
import os

class CameraLidarVideoRecorder(Node):
    def __init__(self):
        super().__init__('camera_lidar_video_recorder')

        self.camera_subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)

        self.lidar_subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10)

        self.video_filename = f'camera_lidar_video_{datetime.now().strftime("%Y%m%d_%H%M%S")}.avi'
        self.bridge = CvBridge()
        self.fps = 10
        self.frame_size = (640, 480)
        self.out = cv2.VideoWriter(
            self.video_filename,
            cv2.VideoWriter_fourcc(*'XVID'),
            self.fps,
            self.frame_size
        )

        self.lidar_data = None
        self.frame_count = 0

        self.dataset_filename = f'camera_lidar_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        self.create_dataset()

        self.get_logger().info(f"Запись видео начата: {self.video_filename}")

    def create_dataset(self):
        with open(self.dataset_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['frame', 'object_x', 'object_y', 'distance'])

    def save_to_dataset(self, frame_id, objects):
        with open(self.dataset_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            for obj in objects:
                writer.writerow([frame_id, obj[0], obj[1], obj[2]]) 
    def lidar_callback(self, msg):
        self.lidar_data = msg

    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            objects = []
            if self.lidar_data:
                frame, objects = self.overlay_lidar_data(frame, self.lidar_data)

            self.out.write(frame)
            self.save_to_dataset(self.frame_count, objects)
            self.frame_count += 1

        except Exception as e:
            self.get_logger().error(f"Ошибка обработки кадра: {e}")

    def overlay_lidar_data(self, frame, lidar_data):
        height, width, _ = frame.shape
        center_x, center_y = width // 2, height // 2

        angle_min = lidar_data.angle_min
        angle_increment = lidar_data.angle_increment
        ranges = np.array(lidar_data.ranges)

        points = []
        for i, r in enumerate(ranges):
            if 0.1 < r < 10.0:
                angle = angle_min + i * angle_increment
                x = r * math.cos(angle)
                y = r * math.sin(angle)
                points.append([x, y])

        objects = []
        if len(points) > 0:
            points = np.array(points)
            clustering = DBSCAN(eps=0.5, min_samples=5).fit(points)
            labels = clustering.labels_

            for label in set(labels):
                if label == -1: 
                    continue
                cluster_points = points[labels == label]
                center = np.mean(cluster_points, axis=0)

                x_screen = int(center_x + center[0] * 100)
                y_screen = int(center_y - center[1] * 100)

                if 0 <= x_screen < width and 0 <= y_screen < height:
                    cv2.line(frame, (center_x, center_y), (x_screen, y_screen), (0, 255, 0), 2)
                    distance = math.sqrt(center[0] ** 2 + center[1] ** 2)
                    cv2.putText(frame, f"{distance:.2f}m", (x_screen, y_screen - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

                    objects.append((center[0], center[1], distance))

        return frame, objects

    def destroy_node(self):
        self.out.release()
        self.get_logger().info(f"Запись видео завершена: {self.video_filename}")
        self.get_logger().info(f"Датасет сохранён: {self.dataset_filename}")
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CameraLidarVideoRecorder()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

