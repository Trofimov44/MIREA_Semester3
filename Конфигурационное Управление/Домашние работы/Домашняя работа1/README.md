## Задание 1 вариант 27
``` python
from zipfile import ZipFile, ZIP_DEFLATED
import shutil
import os
import csv
import datetime

# Словарь для хранения прав доступа к файлам (эмулируем chmod)
file_permissions = {}

def ls(myzip, current_dir):
    listed = set()  # Множество для хранения уникальных имен
    for name in myzip.namelist():
        if name.startswith(current_dir):
            relative_name = name[len(current_dir):].split('/')[0]
            if relative_name not in listed:
                perms = file_permissions.get(name, "default")
                print(f"{relative_name} (permissions: {perms})")
                listed.add(relative_name)


# Функция для записи в лог-файл
def log_action(logfile, user, action, target=""):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(logfile, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, user, action, target])


def du(myzip, dir_path):
    total_size = 0
    for name in myzip.namelist():
        if name.startswith(dir_path):
            info = myzip.getinfo(name)
            total_size += info.file_size
    return total_size


def chmod(file_path, permissions, logfile, user):
    file_permissions[file_path] = permissions
    print(f"Права доступа для {file_path} изменены на {permissions}")

    log_action(logfile, user, f"chmod {permissions}", file_path)


# Функция для перемещения файла в zip-архиве
def mv(zipfile, src, dst, logfile, user):
    with ZipFile(zipfile, 'r') as myzip:
        try:
            content = myzip.read(src)
        except KeyError:
            print(f"mv: {src}: Нет такого файла")
            return

    temp_zip = "temp.zip"
    with ZipFile(zipfile, 'r') as myzip, ZipFile(temp_zip, 'w') as newzip:
        for item in myzip.infolist():
            if item.filename != src:
                newzip.writestr(item, myzip.read(item.filename))

    with ZipFile(temp_zip, 'a') as newzip:
        newzip.writestr(dst, content)

    shutil.move(temp_zip, zipfile)

    if src in file_permissions:
        file_permissions[dst] = file_permissions.pop(src)

    print(f"Файл перемещён из {src} в {dst}")
    log_action(logfile, user, f"mv {src} {dst}")


def main(zipfile, logfile, user):
    current_dir = ""

    with open(logfile, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'User', 'Action', 'Target'])

    while True:
        command = input(f"> {zipfile}/{current_dir} ")

        with ZipFile(zipfile, 'r') as myzip:
            if command == 'ls':
                ls(myzip, current_dir)
                log_action(logfile, user, "ls", current_dir)

            elif command.startswith('cat '):
                file_path = command.split()[1]
                full_path = current_dir + file_path if not file_path.startswith('/') else file_path
                try:
                    content = myzip.read(full_path).decode()
                    print(content)
                    log_action(logfile, user, "cat", file_path)
                except KeyError:
                    print(f"cat: {file_path}: Нет такого файла")

            elif command.startswith('cd '):
                target_dir = command.split()[1]
                if target_dir == "/":
                    current_dir = ""
                else:
                    if target_dir.startswith("/"):
                        new_dir = target_dir.strip("/") + "/"
                    else:
                        new_dir = (current_dir + target_dir).strip("/") + "/"

                    if any(name.startswith(new_dir) for name in myzip.namelist()):
                        current_dir = new_dir
                    else:
                        print(f"cd: {target_dir}: Нет такого файла или каталога")

                log_action(logfile, user, "cd", target_dir)

            elif command == "du":
                size = du(myzip, current_dir)
                print(f"Размер текущей директории: {size} байт")
                log_action(logfile, user, "du", current_dir)

            elif command.startswith("chmod "):
                _, permissions, file_path = command.split()
                full_path = current_dir + file_path if not file_path.startswith('/') else file_path.strip('/')
                chmod(full_path, permissions, logfile, user)

            elif command.startswith("mv "):
                _, src, dst = command.split()
                full_src = current_dir + src if not src.startswith('/') else src.strip('/')
                full_dst = current_dir + dst if not dst.startswith('/') else dst.strip('/')
                mv(zipfile, full_src, full_dst, logfile, user)

            elif command == "exit":
                log_action(logfile, user, "exit")

                # Очистка CSV файла перед выходом
                with open(logfile, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Timestamp', 'User', 'Action', 'Target'])

                print("Программа завершена, лог файл очищен.")
                break

            else:
                print(f"Неизвестная команда: {command}")
                log_action(logfile, user, f"unknown command: {command}")


if __name__ == "__main__":
    zipfile = "files.zip"
    logfile = "session_log.csv"
    user = "user1"

    main(zipfile, logfile, user)
```
# Пример работы команды ls
![изображение](https://github.com/user-attachments/assets/fc6e2f5b-e352-4775-87f8-6855f79c2d81)

# Пример работы cd
![изображение](https://github.com/user-attachments/assets/a8889d7f-ef49-45cd-959e-6b0c61f12d80)

# Пример работы du
![изображение](https://github.com/user-attachments/assets/def05e9b-b53d-4581-8804-ea25216b50f5)

# Пример работы mv
![изображение](https://github.com/user-attachments/assets/03b21fae-2e14-474d-b6fd-48a4ae86b658)

# Пример работы chmod
![изображение](https://github.com/user-attachments/assets/f5d87b53-91c3-497f-b1fd-088d401dbaf2)

# Пример работы exit
![изображение](https://github.com/user-attachments/assets/3ae8c06a-75ae-4baa-871b-54704254edf3)

# Пример лог-файла
![изображение](https://github.com/user-attachments/assets/029fbb0b-725b-49bc-baaa-91739553db20)





