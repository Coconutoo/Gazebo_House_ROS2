import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Image
import math
import pandas as pd
from sqlalchemy import create_engine
import cv2


engine = create_engine("postgresql+psycopg2://user221:123456@localhost:5432/ros", echo=False)

camera_table = {
        'timestamp':[],
        'image':[]
        }
        
class CameraProcessor(Node):
    def __init__(self):
        super().__init__(node_name='camera_processor')
        self.subscription = self.create_subscription(
                Image,
                '/camera/image_raw',
                self.camera_callback,
                10
        )


    def camera_callback(self, msg):
        global camera_table
        # Получение картинки
        timestamp = f'{msg.header.stamp.sec}:{msg.header.stamp.nanosec}'
        image = msg.data
        camera_table['timestamp'].append(timestamp)
        camera_table['image'].append(bytes(image))



def main(args=None):
    try:
        rclpy.init(args=args)
        node_camera = CameraProcessor()
        rclpy.spin(node_camera)
        node_camera.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        camera_frame = pd.DataFrame(camera_table)
        print(camera_frame.head())
        camera_frame.to_sql(name='camera', con=engine, if_exists='append')
        
        
if __name__ == '__main__':
    main()
