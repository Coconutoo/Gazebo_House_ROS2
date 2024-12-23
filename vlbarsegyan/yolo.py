import psycopg2
from ultralytics import YOLO
import cv2
import numpy as np
import os
import pandas as pd

model = YOLO('yolov8n.pt')


colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
    (255, 0, 255), (192, 192, 192), (128, 128, 128), (128, 0, 0), (128, 128, 0),
    (0, 128, 0), (128, 0, 128), (0, 128, 128), (0, 0, 128), (72, 61, 139),
    (47, 79, 79), (47, 79, 47), (0, 206, 209), (148, 0, 211), (255, 20, 147)
]


def process_image(image_path):
    image = cv2.imread(image_path)
    results = model(image)[0]
    
    image = results.orig_img
    classes_names = results.names
    classes = results.boxes.cls.cpu().numpy()
    boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)

    grouped_objects = {}

    for class_id, box in zip(classes, boxes):
        class_name = classes_names[int(class_id)]
        color = colors[int(class_id) % len(colors)]
        if class_name not in grouped_objects:
            grouped_objects[class_name] = []
        grouped_objects[class_name].append(box)

        x1, y1, x2, y2 = box
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    new_image_path = os.getcwd() + '/predictions/' + os.path.splitext(image_path)[0] + '_yolo' + os.path.splitext(image_path)[1]
    cv2.imwrite(new_image_path, image)

    print(f"Processed {image_path}:")
    print(f"Saved bounding-box image to {new_image_path}")


conn = psycopg2.connect(dbname='ros', user='user221', password='123456', host='localhost')
images = pd.read_sql_query('SELECT img_path FROM camera', conn)['img_path'].to_list()
for img_path in images:
    process_image(img_path)
