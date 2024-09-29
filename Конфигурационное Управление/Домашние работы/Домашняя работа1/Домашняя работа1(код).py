from zipfile import ZipFile, ZIP_DEFLATED
import shutil
import os
import csv
import datetime

# Словарь для хранения прав доступа к файлам (эмулируем chmod)
file_permissions = {}


# Функция для записи в лог-файл
# Параметры:
# logfile — путь к файлу для записи лога
# user — пользователь, выполняющий действие
# action — действие, которое было выполнено
# target — цель действия (если есть)
def log_action(logfile, user, action, target=""):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Текущее время
    with open(logfile, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, user, action, target])  # Запись действия в лог


# Функция для подсчета общего размера файлов в директории внутри zip-архива
# Параметры:
# myzip — объект ZipFile
# dir_path — путь к директории
# Возвращает общий размер файлов в байтах
def du(myzip, dir_path):
    total_size = 0
    for name in myzip.namelist():  # Перебираем все файлы в архиве
        if name.startswith(dir_path):  # Проверяем, принадлежит ли файл директории
            info = myzip.getinfo(name)
            total_size += info.file_size  # Суммируем размер файлов
    return total_size


# Функция для перемещения файла в другую директорию внутри zip-архива
# Параметры:
# myzip_path — путь к zip-архиву
# current_dir — текущая директория
# source — исходный файл
# destination — конечная директория
# logfile — путь к файлу лога
# user — пользователь, выполняющий действие
def move_file(myzip_path, current_dir, source, destination, logfile, user):
    with ZipFile(myzip_path, 'r') as myzip:
        # Формируем путь к исходному файлу и конечному месту назначения
        source_path = current_dir + source if not source.startswith('/') else source.strip('/')
        destination_path = current_dir + destination if not destination.startswith('/') else destination.strip('/')

        try:
            file_data = myzip.read(source_path)  # Чтение файла из архива
        except KeyError:
            print(f"mv: {source}: Нет такого файла")  # Ошибка, если файл не найден
            return

        temp_zip_path = "temp.zip"
        # Создаем новый временный архив и копируем туда все файлы кроме перемещаемого
        with ZipFile(temp_zip_path, 'w', ZIP_DEFLATED) as temp_zip:
            for item in myzip.infolist():
                if item.filename != source_path:
                    temp_zip.writestr(item, myzip.read(item.filename))
            temp_zip.writestr(destination_path, file_data)  # Записываем файл в новое место

        # Обновляем права доступа для перемещенного файла
        if source_path in file_permissions:
            file_permissions[destination_path] = file_permissions.pop(source_path)

    shutil.move(temp_zip_path, myzip_path)  # Перемещаем временный архив на место исходного
    print(f"{source} перемещен в {destination}")

    log_action(logfile, user, f"mv {source} {destination}")  # Логируем перемещение


# Функция для изменения прав доступа на файл
# Параметры:
# file_path — путь к файлу
# permissions — права доступа
# logfile — путь к файлу лога
# user — пользователь, выполняющий действие
def chmod(file_path, permissions, logfile, user):
    file_permissions[file_path] = permissions  # Сохраняем новые права доступа
    print(f"Права доступа для {file_path} изменены на {permissions}")

    log_action(logfile, user, f"chmod {permissions}", file_path)  # Логируем изменение прав


# Основной цикл программы — симуляция оболочки для работы с zip-архивом
# Параметры:
# zipfile — путь к zip-архиву
# logfile — путь к файлу лога
# user — пользователь, работающий с архивом
def main(zipfile, logfile, user):
    with ZipFile(zipfile, 'a') as myzip:  # Открываем архив в режиме добавления
        current_dir = ""  # Текущая директория по умолчанию

        # Открываем лог-файл и записываем заголовки столбцов
        with open(logfile, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'User', 'Action', 'Target'])

        while True:
            # Чтение команды от пользователя
            command = input(f"> {zipfile}/{current_dir} ")

            # Команда "ls" для отображения содержимого текущей директории
            if command == 'ls':
                for name in myzip.namelist():
                    if name.startswith(current_dir):
                        relative_name = name[len(current_dir):].split('/')[0]  # Извлечение относительного пути
                        perms = file_permissions.get(name, "default")  # Получение прав доступа
                        print(f"{relative_name} (permissions: {perms})")

                log_action(logfile, user, "ls", current_dir)

            # Команда "cat" для вывода содержимого файла
            elif command.startswith('cat '):
                file_path = command.split()[1]
                full_path = current_dir + file_path if not file_path.startswith('/') else file_path
                try:
                    content = myzip.read(full_path).decode()  # Чтение и вывод содержимого файла
                    print(content)
                    log_action(logfile, user, "cat", file_path)
                except KeyError:
                    print(f"cat: {file_path}: Нет такого файла")

            # Команда "cd" для смены директории
            elif command.startswith('cd '):
                target_dir = command.split()[1]
                if target_dir == "/":
                    current_dir = ""  # Переход в корневую директорию
                else:
                    if target_dir.startswith("/"):
                        new_dir = target_dir.strip("/") + "/"
                    else:
                        new_dir = (current_dir + target_dir).strip("/") + "/"

                    if any(name.startswith(new_dir) for name in myzip.namelist()):  # Проверяем существование директории
                        current_dir = new_dir
                    else:
                        print(f"cd: {target_dir}: Нет такого файла или каталога")

                log_action(logfile, user, "cd", target_dir)

            # Команда "du" для подсчета размера текущей директории
            elif command == "du":
                size = du(myzip, current_dir)
                print(f"Размер текущей директории: {size} байт")
                log_action(logfile, user, "du", current_dir)

            # Команда "mv" для перемещения файла
            elif command.startswith("mv "):
                _, source, destination = command.split()
                move_file(zipfile, current_dir, source, destination, logfile, user)

            # Команда "chmod" для изменения прав доступа
            elif command.startswith("chmod "):
                _, permissions, file_path = command.split()
                full_path = current_dir + file_path if not file_path.startswith('/') else file_path.strip('/')
                chmod(full_path, permissions, logfile, user)

            # Команда "exit" для выхода из программы
            elif command == "exit":
                log_action(logfile, user, "exit")
                break

            # Обработка неизвестных команд
            else:
                print(f"Неизвестная команда: {command}")
                log_action(logfile, user, f"unknown command: {command}")


# Точка входа в программу
if __name__ == "__main__":
    # Пример вызова программы
    zipfile = "files.zip"
    logfile = "session_log.csv"
    user = "user1"

    main(zipfile, logfile, user)
