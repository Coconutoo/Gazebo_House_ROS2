import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Image
import math
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://user221:123456@localhost:5432/ros", echo=False)

lidar_table = {
        'timestamp':[],
        'x':[],
        'y':[]
        }

class LidarProcessor(Node):
    def __init__(self):
        super().__init__(node_name='lidar_processor')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10
        )

    def lidar_callback(self, msg):
        global lidar_table
        # Получение координат объектов
        timestamp = f'{msg.header.stamp.sec}:{msg.header.stamp.nanosec}'
        ranges = msg.ranges
        angle_increment = msg.angle_increment
        for i, distance in enumerate(ranges):
            if 0.1 < distance < 3.5:  # Условие для допустимых данных
                angle = msg.angle_min + i * angle_increment
                x = distance * math.cos(angle)
                y = distance * math.sin(angle)
                lidar_table['timestamp'].append(timestamp)
                lidar_table['x'].append(x)
                lidar_table['y'].append(y)


def main(args=None):
    try:
        rclpy.init(args=args)
        node_lidar = LidarProcessor()
        rclpy.spin(node_lidar)
        node_lidar.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        lidar_frame = pd.DataFrame(lidar_table)
        lidar_frame.to_sql(name='lidar', con=engine, if_exists='append')

if __name__ == '__main__':
    main()
