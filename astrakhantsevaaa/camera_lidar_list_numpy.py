import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Image
from cv_bridge import CvBridge
import sqlite3
import numpy as np
import time
import datetime
import os
import cv2

class DataSaver(Node):
    def __init__(self):
        super().__init__('data_saver')
        self.bridge = CvBridge()
        
        self.create_subscription(LaserScan, '/scan', self.lidar_callback, 10)
        self.create_subscription(Image, '/camera/image_raw', self.camera_callback, 10)

        self.lidar_data = None
        self.camera_frame = None
        self.last_save_time = time.time()

        self.image_dir = "robot_images"
        os.makedirs(self.image_dir, exist_ok=True)

        try:
            self.conn = sqlite3.connect('robot_data.db')
            self.cursor = self.conn.cursor()
            
            self.cursor.execute('DROP TABLE IF EXISTS data')
            
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                                    timestamp TEXT,  
                                    camera_image BLOB,
                                    lidar_data BLOB)''')
            self.conn.commit()
            self.get_logger().info("Database initialized successfully.")
        except sqlite3.Error as e:
            self.get_logger().error(f"Database connection error: {e}")
            return

    def lidar_callback(self, msg):
 
        self.lidar_data = np.array(msg.ranges)

    def camera_callback(self, msg):

        self.camera_frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        self.save_data()

    def save_data(self):
        current_time = time.time()
        if current_time - self.last_save_time >= 5: 
            if self.lidar_data is not None and self.camera_frame is not None:
                try:
                    readable_time = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H-%M-%S')
                    
                    lidar_blob = self.lidar_data.tobytes()
                    image_blob = self.camera_frame.tobytes()

                    image_filename = os.path.join(self.image_dir, f"image_{readable_time}.jpg")
                    cv2.imwrite(image_filename, self.camera_frame)
                    self.get_logger().info(f"Image saved to: {image_filename}")

                    self.cursor.execute("INSERT INTO data (timestamp, camera_image, lidar_data) VALUES (?, ?, ?)",
                                        (readable_time, image_blob, lidar_blob))
                    self.conn.commit()
                    self.get_logger().info(f"Data saved at {readable_time}")

                    self.last_save_time = current_time
                except sqlite3.Error as e:
                    self.get_logger().error(f"Database insertion error: {e}")
                except cv2.error as e:
                    self.get_logger().error(f"OpenCV error: {e}")

def main(args=None):
    rclpy.init(args=args)
    data_saver = DataSaver()
    rclpy.spin(data_saver)
    data_saver.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

