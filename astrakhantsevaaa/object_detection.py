import os
import cv2
import torch

IMAGE_DIR = "robot_images"
OUTPUT_DIR = "detected_objects"
os.makedirs(OUTPUT_DIR, exist_ok=True)

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)


for filename in os.listdir(IMAGE_DIR):
    if filename.endswith(".jpg"):
        image_path = os.path.join(IMAGE_DIR, filename)
        image = cv2.imread(image_path)

        results = model(image)

        annotated_image = results.render()[0]

        output_image_path = os.path.join(OUTPUT_DIR, filename)
        cv2.imwrite(output_image_path, annotated_image)


        detected_objects = results.pandas().xyxy[0]["name"].tolist()
        description = f"In the image '{filename}', detected objects: {', '.join(detected_objects)}"
        print(description)

        with open(os.path.join(OUTPUT_DIR, "descriptions.txt"), "a") as f:
            f.write(description + "\n")
