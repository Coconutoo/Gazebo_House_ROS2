import psycopg2

try:
    # Параметры подключения
    connection = psycopg2.connect(
        database="lidar_camera_data",
        user="lidar_user",
        password="secure_password",
        host="localhost",
        port="5432"
    )
    print("Соединение с базой данных успешно установлено!")

    # Закрываем соединение
    connection.close()
    print("Соединение закрыто.")
except psycopg2.OperationalError as e:
    print("Ошибка подключения к базе данных:")
    print(e)

