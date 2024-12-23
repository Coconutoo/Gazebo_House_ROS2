import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Image
import math
import pandas as pd
from sqlalchemy import create_engine
import cv2
from time import sleep
from cv_bridge import CvBridge, CvBridgeError
import os.path

engine = create_engine("postgresql+psycopg2://user221:123456@localhost:5432/ros", echo=False)

camera_table = {
        'timestamp':[],
        'img_path':[]
        }
k = 0

class CameraProcessor(Node):
    def __init__(self):
        super().__init__(node_name='camera_processor')
        self.subscription = self.create_subscription(
                Image,
                '/camera/image_raw',
                self.camera_callback,
                10
        )
        self.bridge = CvBridge()


    def camera_callback(self, msg):
        global camera_table, k
        # Получение картинки
        timestamp = f'{msg.header.stamp.sec}:{msg.header.stamp.nanosec}'
        image = msg.data
        print('got cb')
        cv2_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        cv2.imwrite(f'data/img{k}.jpeg', cv2_img)
        k += 1
        
        camera_table['timestamp'].append(timestamp)
        camera_table['img_path'].append(f'data/img{k}.jpeg')
        sleep(1)


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
