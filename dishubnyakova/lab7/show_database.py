import sqlite3
import numpy as np
import cv2
import math

def calculate_distance(x, y):
    return math.sqrt(x**2 + y**2)

def show_database():
    conn = sqlite3.connect('robot_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT timestamp, image, lidar_coordinates FROM robot_data')
    records = cursor.fetchall()

    print("База данных: robot_data.db\n")
    
    for record in records:
        timestamp, image_bytes, lidar_bytes = record

        # Обработка изображения
        try:
            image_np = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
            if image_np is None:
                print(f"Ошибка декодирования изображения для времени: {timestamp}")
                continue
        except Exception as e:
            print(f"Ошибка обработки изображения: {e}")
            continue

        # Обработка LIDAR данных
        try:
            lidar_data = np.frombuffer(lidar_bytes, dtype=np.float32).reshape(-1, 2)
        except Exception as e:
            print(f"Ошибка обработки данных LIDAR: {e}")
            continue

        # Вывод информации
        print(f"1. Время: {timestamp}")
        print(f"2. Представление изображения в NumPy:")
        print(image_np)
        print(f"3. Координаты LIDAR (x, y):")
        print(lidar_data)
        print(f"4. Расстояние до объекта:")
        
        for i, (x, y) in enumerate(lidar_data):
            distance = calculate_distance(x, y)
            print(f" Точка {i+1}: ({x:.2f}, {y:.2f}) -> Расстояние: {distance:.2f} м")
        
        print("\n" + "="*50 + "\n")

        # Показ изображения
        cv2.imshow(f"Изображение на {timestamp}", image_np)
        cv2.waitKey(0)  # Ожидание нажатия клавиши
        cv2.destroyAllWindows()  # Закрытие окна после отображения

    conn.close()

if __name__ == "__main__":
    show_database()

