import unittest
import os
from zipfile import ZipFile
import shutil
from io import StringIO
from contextlib import redirect_stdout

# Импортируем функции из основной программы
from main_program import ls, chmod, mv, du, log_action

class TestZipFileOperations(unittest.TestCase):

    def setUp(self):
        # Создаем тестовый zip файл
        self.test_zip = "test_files.zip"
        self.test_log = "test_log.csv"
        self.user = "test_user"

        # Создаем ZIP файл с тестовыми данными
        with ZipFile(self.test_zip, 'w') as myzip:
            myzip.writestr("test1.txt", "This is test file 1.")
            myzip.writestr("test2.txt", "This is test file 2.")
            myzip.writestr("dir/test3.txt", "This is test file 3 in a directory.")

        # Создаем пустой лог-файл
        with open(self.test_log, 'w') as f:
            f.write("Timestamp,User,Action,Target\n")

    def tearDown(self):
        # Удаляем тестовые файлы после выполнения тестов
        if os.path.exists(self.test_zip):
            os.remove(self.test_zip)
        if os.path.exists(self.test_log):
            os.remove(self.test_log)

    def test_ls(self):
        with ZipFile(self.test_zip, 'r') as myzip:
            # Перенаправляем вывод в переменную
            output = StringIO()
            with redirect_stdout(output):
                ls(myzip, "")
            # Проверяем содержимое вывода
            result = output.getvalue().strip().split("\n")
            self.assertIn("test1.txt", result)
            self.assertIn("test2.txt", result)
            self.assertIn("dir", result)

    def test_du(self):
        with ZipFile(self.test_zip, 'r') as myzip:
            size = du(myzip, "")
            # Проверяем, что размер не нулевой
            self.assertGreater(size, 0)

    def test_chmod(self):
        with ZipFile(self.test_zip, 'r') as myzip:
            file_path = "test1.txt"
            permissions = "755"
            chmod(myzip, file_path, permissions, self.test_log, self.user)
            # Проверяем, что права доступа изменены в словаре file_permissions
            self.assertEqual(file_permissions[file_path], permissions)

    def test_mv(self):
        src = "test1.txt"
        dst = "new_test1.txt"
        mv(self.test_zip, src, dst, self.test_log, self.user)
        # Открываем ZIP архив и проверяем, что файл перемещен
        with ZipFile(self.test_zip, 'r') as myzip:
            self.assertIn(dst, myzip.namelist())
            self.assertNotIn(src, myzip.namelist())

    def test_log_action(self):
        # Логируем действие
        log_action(self.test_log, self.user, "test_action", "test_target")
        # Проверяем, что запись добавлена в лог-файл
        with open(self.test_log, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)  # Должно быть две строки (заголовок + запись)

if __name__ == '__main__':
    unittest.main()
