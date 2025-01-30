import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math
import numpy as np

class LidarToCoordinates(Node):
    def __init__(self):
        super().__init__('lidar_to_coordinates')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        self.lidar_coordinates = None

    def scan_callback(self, msg):
        angle = msg.angle_min
        coordinates = []

        for distance in msg.ranges:
            if msg.range_min <= distance <= msg.range_max:
                x = distance * math.cos(angle)
                y = distance * math.sin(angle)
                coordinates.append((x, y))
            angle += msg.angle_increment

        self.lidar_coordinates = np.array(coordinates)
        self.get_logger().info(f'LIDAR coordinates updated: {len(coordinates)} points.')

    def get_coordinates(self):
        return self.lidar_coordinates

def main(args=None):
    rclpy.init(args=args)
    node = LidarToCoordinates()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
