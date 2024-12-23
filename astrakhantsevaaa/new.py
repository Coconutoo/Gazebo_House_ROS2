import os
from PIL import Image, ImageDraw, ImageFont
import torch
from torchvision import models, transforms
import requests  


image_dir = "robot_images"
output_dir = "output_resnet"
os.makedirs(output_dir, exist_ok=True)


model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
model.eval() 

url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
response = requests.get(url)

if response.status_code == 200:
    imagenet_classes = response.json()
else:
    raise Exception("Не удалось загрузить метки классов ImageNet.")


preprocess = transforms.Compose([
    transforms.Resize((224, 224)),  
    transforms.ToTensor(), 
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406], 
        std=[0.229, 0.224, 0.225]
    )
])


font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font = ImageFont.truetype(font_path, size=20)


for image_file in os.listdir(image_dir):
    if not image_file.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    image_path = os.path.join(image_dir, image_file)
    img = Image.open(image_path)

    input_tensor = preprocess(img).unsqueeze(0) 

    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)  
        top5_prob, top5_catid = torch.topk(probabilities, 5)

    descriptions = [f"{imagenet_classes[catid]}: {prob:.2f}" for prob, catid in zip(top5_prob, top5_catid)]

    draw = ImageDraw.Draw(img)
    text_position = (10, 10)
    for i, description in enumerate(descriptions):
        draw.text((10, 10 + i * 25), description, fill="red", font=font)

    output_path = os.path.join(output_dir, image_file)
    img.save(output_path)

    print(f"Обработано изображение: {image_file}, результат сохранён в {output_path}")

print(f"Визуализация завершена. Результаты сохранены в папке {output_dir}.")
