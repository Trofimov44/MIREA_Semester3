from zipfile import ZipFile, ZIP_DEFLATED
import shutil
import os
import csv
import datetime

# Словарь для хранения прав доступа к файлам (эмулируем chmod)
file_permissions = {}


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


def move_file(myzip_path, current_dir, source, destination, logfile, user):
    with ZipFile(myzip_path, 'r') as myzip:
        source_path = current_dir + source if not source.startswith('/') else source.strip('/')
        destination_path = current_dir + destination if not destination.startswith('/') else destination.strip('/')

        try:
            file_data = myzip.read(source_path)
        except KeyError:
            print(f"mv: {source}: Нет такого файла")
            return

        temp_zip_path = "temp.zip"
        with ZipFile(temp_zip_path, 'w', ZIP_DEFLATED) as temp_zip:
            for item in myzip.infolist():
                if item.filename != source_path:
                    temp_zip.writestr(item, myzip.read(item.filename))
            temp_zip.writestr(destination_path, file_data)

        if source_path in file_permissions:
            file_permissions[destination_path] = file_permissions.pop(source_path)

    shutil.move(temp_zip_path, myzip_path)
    print(f"{source} перемещен в {destination}")

    log_action(logfile, user, f"mv {source} {destination}")


def chmod(file_path, permissions, logfile, user):
    file_permissions[file_path] = permissions
    print(f"Права доступа для {file_path} изменены на {permissions}")

    log_action(logfile, user, f"chmod {permissions}", file_path)


# Основной цикл программы
def main(zipfile, logfile, user):
    with ZipFile(zipfile, 'a') as myzip:
        current_dir = ""

        # Открываем лог-файл для записи действий
        with open(logfile, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'User', 'Action', 'Target'])

        while True:
            command = input(f"> {zipfile}/{current_dir} ")

            if command == 'ls':
                for name in myzip.namelist():
                    if name.startswith(current_dir):
                        relative_name = name[len(current_dir):].split('/')[0]
                        perms = file_permissions.get(name, "default")
                        print(f"{relative_name} (permissions: {perms})")

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

            elif command.startswith("mv "):
                _, source, destination = command.split()
                move_file(zipfile, current_dir, source, destination, logfile, user)

            elif command.startswith("chmod "):
                _, permissions, file_path = command.split()
                full_path = current_dir + file_path if not file_path.startswith('/') else file_path.strip('/')
                chmod(full_path, permissions, logfile, user)

            elif command == "exit":
                log_action(logfile, user, "exit")
                break

            else:
                print(f"Неизвестная команда: {command}")
                log_action(logfile, user, f"unknown command: {command}")


if __name__ == "__main__":
    # Пример вызова программы
    zipfile = "files.zip"
    logfile = "session_log.csv"
    user = "user1"

    main(zipfile, logfile, user)
