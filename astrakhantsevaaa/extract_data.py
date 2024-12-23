import sqlite3
import numpy as np
import cv2
import os

IMAGE_DIR = "extracted_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

conn = sqlite3.connect('robot_data.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM data")
rows = cursor.fetchall()

for row in rows:
    timestamp = row[0]  
    image_blob = row[1]  
    lidar_blob = row[2] 
    
    print(f"Timestamp: {timestamp}")

    nparr = np.frombuffer(image_blob, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    lidar_data = np.frombuffer(lidar_blob, dtype=np.float32)
    print(f"Lidar data (first 10 values): {lidar_data[:10]}")  

    if img is not None and img.size > 0: 
        image_filename = os.path.join(IMAGE_DIR, f"image_{timestamp.replace(':', '-')}.jpg")
        cv2.imwrite(image_filename, img)
        print(f"Image saved to: {image_filename}")
    else:
        print(f"Image is empty for timestamp {timestamp}, skipping save.")

    print("-" * 20)

conn.close()

