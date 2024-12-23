import os
from ultralytics import YOLO
import csv
from datetime import datetime

# Путь к папке с изображениями
image_dir = "images"
output_dir = "output_descriptions"
os.makedirs(output_dir, exist_ok=True)

# Загрузка модели YOLOv8
model = YOLO("yolov8n.pt")

# Файл для сохранения описаний
output_file = os.path.join(output_dir, f"description_{datetime.now().strftime('%Y%m%d')}.txt")

# Открытие файла для записи описаний
with open(output_file, "w", encoding="utf-8") as f:
    # Цикл по всем изображениям в папке
    for image_file in os.listdir(image_dir):
        # Полный путь к файлу
        image_path = os.path.join(image_dir, image_file)

        # Убедимся, что это файл изображения
        if not image_file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue  # Пропустить, если файл не изображение

        print(f"Обрабатывается изображение: {image_path}")

        # Запуск детекции объектов на изображении
        results = model(image_path)

        # Получение описаний объектов
        for result in results:
            if result.boxes:
                detected_objects = [model.names[int(cls)] for cls in result.boxes.cls]
                description = f"На изображении {image_file} обнаружены: {', '.join(detected_objects)}."
            else:
                description = f"На изображении {image_file} объектов не обнаружено."

            # Запись описания в файл
            f.write(description + "\n")
            print(f"Сохранено описание: {description}")

print(f"Все описания сохранены в файл: {output_file}")

