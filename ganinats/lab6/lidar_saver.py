import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import csv

class LidarSaver(Node):
    def __init__(self):
        super().__init__('lidar_saver')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            10)
        self.csv_file = open('lidar_data.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Angle', 'Distance'])

    def listener_callback(self, msg):
        angle = msg.angle_min
        for r in msg.ranges:
            self.csv_writer.writerow([angle, r])
            angle += msg.angle_increment
        self.get_logger().info('Lidar data saved.')

    def destroy_node(self):
        self.csv_file.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = LidarSaver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

