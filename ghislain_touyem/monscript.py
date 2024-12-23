import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Image
from cv_bridge import CvBridge
import cv2
import math
import os
from datetime import datetime
import json

class DataRecorder(Node):
    def __init__(self):
        super().__init__('data_recorder')
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.image_sub = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.bridge = CvBridge()
        self.output_dir = 'recorded_data'
        os.makedirs(self.output_dir, exist_ok=True)
        self.image_count = 0

    def scan_callback(self, msg):
      timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
      object_data = []
      for i, distance in enumerate(msg.ranges):
          if distance != float('inf') and distance > msg.range_min and distance < msg.range_max:
              angle = msg.angle_min + i * msg.angle_increment
              x = distance * math.cos(angle)
              y = distance * math.sin(angle)
              object_data.append({'x': x, 'y': y})

        # Save in file, format depends on your need. Here's a json example
      if object_data:
         filename = os.path.join(self.output_dir, f"scan_{timestamp}.json")
         with open(filename, 'w') as f:
           json.dump(object_data, f)
        # Note that we call save_image only if an image has been received by a previous image callback. This is not ideal (see comments below), but it's good for this example.
         if hasattr(self, 'last_image'):
           self.save_image(self.last_image, timestamp)

    def image_callback(self, msg):
       self.last_image = msg

    def save_image(self, msg, timestamp):
      try:
          cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
          filename = os.path.join(self.output_dir, f"image_{timestamp}.jpg")
          cv2.imwrite(filename, cv_image)
          self.image_count += 1
          self.get_logger().info(f"Image {self.image_count} saved with timestamp {timestamp}")
      except Exception as e:
          self.get_logger().error(f"Error during image save {e}")


def main(args=None):
    rclpy.init(args=args)
    data_recorder = DataRecorder()
    rclpy.spin(data_recorder)
    data_recorder.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
