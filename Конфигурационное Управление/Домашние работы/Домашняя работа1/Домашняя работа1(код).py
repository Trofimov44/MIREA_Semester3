from zipfile import ZipFile, ZIP_DEFLATED
import shutil
import os
import csv
import datetime

# Словарь для хранения прав доступа к файлам (эмулируем chmod)
file_permissions = {}

# Функция для перевода числовых прав в строковой формат (rwx)
def permissions_to_str(perm):
    perm = int(perm, 8)  # Преобразуем восьмеричное число в целое
    perms_str = ""
    # Права владельца
    perms_str += 'r' if perm & 0o400 else '-'
    perms_str += 'w' if perm & 0o200 else '-'
    perms_str += 'x' if perm & 0o100 else '-'
    # Права группы
    perms_str += 'r' if perm & 0o040 else '-'
    perms_str += 'w' if perm & 0o020 else '-'
    perms_str += 'x' if perm & 0o010 else '-'
    # Права для остальных
    perms_str += 'r' if perm & 0o004 else '-'
    perms_str += 'w' if perm & 0o002 else '-'
    perms_str += 'x' if perm & 0o001 else '-'
    return perms_str

# Функция для вывода списка файлов в zip-архиве
def ls_l(myzip, current_dir):
    listed = set()  # Множество для хранения уникальных имен
    for name in myzip.namelist():
        # Проверяем, начинается ли имя файла с текущей директории
        if name.startswith(current_dir):
            # Получаем относительное имя файла/папки
            relative_name = name[len(current_dir):].split('/')[0]
            if relative_name not in listed:
                # Получаем права доступа для файла
                perms = file_permissions.get(name, "default")
                perms_str = permissions_to_str(perms) if perms != "default" else "rw-r--r--"
                print(f"{perms_str} {relative_name}")
                listed.add(relative_name)
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
                perms_str = permissions_to_str(perms) if perms != "default" else "rw-r--r--"
                print(f"{relative_name}")
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
def chmod(myzip, file_path, permissions, logfile, user):
    try:
        # Проверяем наличие всех аргументов
        if not permissions or not file_path:
            raise ValueError(
                "Ошибка: Команда chmod требует указания как прав доступа, так и имени файла. Пример: chmod 755 test.txt")

        # Проверяем корректность переданных прав доступа
        if len(permissions) != 3 or not permissions.isdigit():
            raise ValueError(
                "Неправильный формат прав доступа. Используйте числовое восьмеричное значение, например, 755.")

        # Проверяем существование файла в архиве
        if file_path not in myzip.namelist():
            raise FileNotFoundError(f"Ошибка: Файл {file_path} не найден в архиве.")

        # Устанавливаем права доступа
        file_permissions[file_path] = permissions
        print(f"Права доступа для {file_path} изменены на {permissions_to_str(permissions)}")
        log_action(logfile, user, f"chmod {permissions}", file_path)  # Логируем изменение

    except (ValueError, FileNotFoundError) as e:
        print(e)


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
            if command == 'ls -l':
                ls_l(myzip, current_dir)  # Выводим список файлов
                log_action(logfile, user, "ls", current_dir)
            elif command == 'ls':
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
                parts = command.split()
                if len(parts) != 3:
                    print(
                        "Ошибка: команда chmod требует указания прав доступа и имени файла. Пример: chmod 755 test.txt")
                else:
                    _, permissions, file_path = parts
                    full_path = current_dir + file_path if not file_path.startswith('/') else file_path.strip('/')
                    chmod(myzip, full_path, permissions, logfile, user)  # Изменяем права доступа


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
