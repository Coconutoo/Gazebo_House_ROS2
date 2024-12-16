import subprocess
import os

def main():
    # Указываем имена скриптов
    scripts = ["union_rgb.py", "union_base64.py", "union_photo.py"]

    # Получаем текущую директорию
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Запускаем каждый скрипт
    processes = []
    for script in scripts:
        script_path = os.path.join(current_dir, script)
        try:
            # Запускаем скрипт как отдельный процесс
            process = subprocess.Popen(["python3", script_path])
            processes.append(process)
            print(f"Запущен скрипт: {script}")
        except Exception as e:
            print(f"Ошибка при запуске {script}: {e}")

    # Ожидаем завершения всех процессов
    for process in processes:
        process.wait()

    print("Все скрипты завершены.")

if __name__ == "__main__":
    main()

