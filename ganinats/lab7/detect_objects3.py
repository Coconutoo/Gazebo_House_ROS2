import os
from ultralytics import YOLO
from datetime import datetime

image_dir = "images"
output_dir = "output_descriptions"
os.makedirs(output_dir, exist_ok=True)

model = YOLO("yolov8x.pt")

output_file = os.path.join(output_dir, f"description_3.txt")

with open(output_file, "w", encoding="utf-8") as f:
    for image_file in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_file)

        if not image_file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue  # Пропустить, если файл не изображение

        print(f"Обрабатывается изображение: {image_path}")

        results = model(image_path)

        for result in results:
            if result.boxes:
                detected_objects = [
                    model.names[int(cls)] for cls, conf in zip(result.boxes.cls, result.boxes.conf)
                    if conf >= 0.5  # Порог уверенности 0.4
                ]
                if detected_objects:
                    description = f"На изображении {image_file} обнаружены: {', '.join(detected_objects)}."
                else:
                    description = f"На изображении {image_file} объекты с достаточной уверенностью не обнаружены."
            else:
                description = f"На изображении {image_file} объектов не обнаружено."

            f.write(description + "\n")
            print(f"Сохранено описание: {description}")

print(f"Все описания сохранены в файл: {output_file}")

