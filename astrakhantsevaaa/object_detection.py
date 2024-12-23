import os
import cv2
import torch
from rsnet import RSNet 

IMAGE_DIR = "robot_images"
OUTPUT_DIR = "detected_objects"
os.makedirs(OUTPUT_DIR, exist_ok=True)


model = RSNet(pretrained=True)  


for filename in os.listdir(IMAGE_DIR):
    if filename.endswith(".jpg"):
        image_path = os.path.join(IMAGE_DIR, filename)
        image = cv2.imread(image_path)

        image_tensor = torch.from_numpy(image).permute(2, 0, 1).unsqueeze(0).float()

        results = model(image_tensor)

        annotated_image = results["annotated_image"]
        detected_objects = results["detected_objects"]

        output_image_path = os.path.join(OUTPUT_DIR, filename)
        cv2.imwrite(output_image_path, annotated_image)

        description = f"In the image '{filename}', detected objects: {', '.join(detected_objects)}"
        print(description)

        with open(os.path.join(OUTPUT_DIR, "descriptions.txt"), "a") as f:
            f.write(description + "\n")

