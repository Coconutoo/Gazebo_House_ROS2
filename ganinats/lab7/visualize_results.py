import os
from PIL import Image, ImageDraw, ImageFont

image_dir = "images"  # Папка с исходными изображениями
description_file = "output_descriptions/description_3.txt"  # Файл с описаниями
output_dir = "output_visualized3"  # Папка для сохранения изображений с описаниями

os.makedirs(output_dir, exist_ok=True)

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Убедитесь, что этот шрифт установлен
font_size = 20  # Размер шрифта
font = ImageFont.truetype(font_path, font_size)

with open(description_file, "r", encoding="utf-8") as f:
    descriptions = f.readlines()

for idx, image_file in enumerate(os.listdir(image_dir)):
    if not image_file.lower().endswith((".png", ".jpg", ".jpeg")):
        continue  # Пропускаем не-изображения

    image_path = os.path.join(image_dir, image_file)
    img = Image.open(image_path)

    draw = ImageDraw.Draw(img)

    if idx < len(descriptions):
        description = descriptions[idx].strip()
    else:
        description = "Описание отсутствует"

    text_position = (10, 10)
    text_color = "red"  # Цвет текста

    draw.text(text_position, description, fill=text_color, font=font)

    output_path = os.path.join(output_dir, image_file)
    img.save(output_path)

print(f"Визуализация завершена. Файлы сохранены в папке: {output_dir}")

