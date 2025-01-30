import sqlite3
import numpy as np
import cv2

def visualize_data():
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('robot_data.db')
    cursor = conn.cursor()

    # Получение всех записей
    cursor.execute('SELECT timestamp, image, lidar_coordinates FROM robot_data')
    records = cursor.fetchall()

    for record in records:
        timestamp, image_bytes, lidar_bytes = record

        print(f"\nВизуализация данных с меткой времени: {timestamp}")

        try:
            # Декодирование сжато изображения в формате JPEG
            image_np = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
            if image_np is None:
                print(f"Ошибка при декодировании изображения с меткой времени {timestamp}")
                continue

            # Восстановление данных LIDAR
            lidar_data = np.frombuffer(lidar_bytes, dtype=np.float32).reshape(-1, 2)

            # Отображение изображения
            cv2.imshow(f'Изображение - {timestamp}', image_np)
            print(f"Координаты LIDAR (первые 5 точек):")
            for point in lidar_data[:1000]:
                print(f"({point[0]:.2f}, {point[1]:.2f})")

            # Ожидание и закрытие окна
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        except Exception as e:
            print(f"Ошибка при обработке данных: {e}")

    conn.close()

if __name__ == '__main__':
    visualize_data()
