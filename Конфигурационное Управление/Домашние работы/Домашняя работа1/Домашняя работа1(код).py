from zipfile import ZipFile, ZIP_DEFLATED
import shutil
import os
import csv
import datetime

# Словарь для хранения прав доступа к файлам (эмулируем chmod)
file_permissions = {}

# Функция для вывода списка файлов в zip-архиве
def ls(myzip, current_dir):
    listed = set()  # Множество для хранения уникальных имен
    for name in myzip.namelist():
        # Проверяем, начинается ли имя файла с текущей директории
        if name.startswith(current_dir):
            # Получаем относительное имя файла/папки
            relative_name = name[len(current_dir):].split('/')[0]
            if relative_name not in listed:
                # Получаем права доступа для файла
                perms = file_permissions.get(name, "default")
                print(f"{relative_name} (permissions: {perms})")
                listed.add(relative_name)

# Функция для записи действия в лог-файл
def log_action(logfile, user, action, target=""):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Получаем текущее время
    with open(logfile, 'a', newline='') as f:  # Открываем лог-файл для записи
        writer = csv.writer(f)
        writer.writerow([timestamp, user, action, target])  # Записываем данные в лог

# Функция для расчета общего размера директории в zip-архиве
def du(myzip, dir_path):
    total_size = 0
    for name in myzip.namelist():
        # Если файл находится в нужной директории
        if name.startswith(dir_path):
            info = myzip.getinfo(name)  # Получаем информацию о файле
            total_size += info.file_size  # Добавляем размер файла к общему
    return total_size  # Возвращаем общий размер

# Функция для изменения прав доступа к файлу
def chmod(file_path, permissions, logfile, user):
    file_permissions[file_path] = permissions  # Устанавливаем права доступа
    print(f"Права доступа для {file_path} изменены на {permissions}")
    log_action(logfile, user, f"chmod {permissions}", file_path)  # Логируем изменение

# Функция для перемещения файла внутри zip-архива
def mv(zipfile, src, dst, logfile, user):
    with ZipFile(zipfile, 'r') as myzip:
        try:
            # Читаем содержимое исходного файла
            content = myzip.read(src)
        except KeyError:
            # Если файл не найден
            print(f"mv: {src}: Нет такого файла")
            return

    temp_zip = "temp.zip"
    # Копируем все файлы, кроме исходного, в новый архив
    with ZipFile(zipfile, 'r') as myzip, ZipFile(temp_zip, 'w') as newzip:
        for item in myzip.infolist():
            if item.filename != src:
                newzip.writestr(item, myzip.read(item.filename))

    # Добавляем перемещенный файл в новый архив
    with ZipFile(temp_zip, 'a') as newzip:
        newzip.writestr(dst, content)

    shutil.move(temp_zip, zipfile)  # Перемещаем временный архив на место оригинального

    # Обновляем права доступа для перемещенного файла
    if src in file_permissions:
        file_permissions[dst] = file_permissions.pop(src)

    print(f"Файл перемещён из {src} в {dst}")
    log_action(logfile, user, f"mv {src} {dst}")  # Логируем перемещение

# Основная функция, реализующая командный интерфейс
def main(zipfile, logfile, user):
    current_dir = ""  # Текущая директория

    # Инициализация лог-файла
    with open(logfile, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'User', 'Action', 'Target'])  # Заголовки для CSV

    while True:
        command = input(f"> {zipfile}/{current_dir} ")  # Ввод команды от пользователя

        with ZipFile(zipfile, 'r') as myzip:
            if command == 'ls':
                ls(myzip, current_dir)  # Выводим список файлов
                log_action(logfile, user, "ls", current_dir)

            elif command.startswith('cat '):
                file_path = command.split()[1]
                # Получаем полный путь к файлу
                full_path = current_dir + file_path if not file_path.startswith('/') else file_path
                try:
                    # Читаем содержимое файла и выводим его
                    content = myzip.read(full_path).decode()
                    print(content)
                    log_action(logfile, user, "cat", file_path)
                except KeyError:
                    # Файл не найден
                    print(f"cat: {file_path}: Нет такого файла")

            elif command.startswith('cd '):
                target_dir = command.split()[1]
                if target_dir == "/":
                    current_dir = ""  # Переход в корневую директорию
                else:
                    # Формируем новый путь к директории
                    if target_dir.startswith("/"):
                        new_dir = target_dir.strip("/") + "/"
                    else:
                        new_dir = (current_dir + target_dir).strip("/") + "/"

                    # Проверяем, существует ли такая директория
                    if any(name.startswith(new_dir) for name in myzip.namelist()):
                        current_dir = new_dir  # Устанавливаем текущую директорию
                    else:
                        print(f"cd: {target_dir}: Нет такого файла или каталога")

                log_action(logfile, user, "cd", target_dir)

            elif command == "du":
                size = du(myzip, current_dir)  # Получаем размер директории
                print(f"Размер текущей директории: {size} байт")
                log_action(logfile, user, "du", current_dir)

            elif command.startswith("chmod "):
                _, permissions, file_path = command.split()
                full_path = current_dir + file_path if not file_path.startswith('/') else file_path.strip('/')
                chmod(full_path, permissions, logfile, user)  # Изменяем права доступа

            elif command.startswith("mv "):
                _, src, dst = command.split()
                full_src = current_dir + src if not src.startswith('/') else src.strip('/')
                full_dst = current_dir + dst if not dst.startswith('/') else dst.strip('/')
                mv(zipfile, full_src, full_dst, logfile, user)  # Перемещаем файл

            elif command == "exit":
                log_action(logfile, user, "exit")  # Логируем выход

                # Очищаем лог-файл перед завершением
                with open(logfile, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Timestamp', 'User', 'Action', 'Target'])

                print("Программа завершена, лог файл очищен.")
                break

            else:
                print(f"Неизвестная команда: {command}")
                log_action(logfile, user, f"unknown command: {command}")  # Логируем неизвестную команду

# Точка входа в программу
if __name__ == "__main__":
    zipfile = "files.zip"  # Имя zip-архива
    logfile = "session_log.csv"  # Имя лог-файла
    user = "user1"  # Имя пользователя

    main(zipfile, logfile, user)  # Запускаем основную функцию
