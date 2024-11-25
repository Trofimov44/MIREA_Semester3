# Описание
Этот проект представляет собой инструмент командной строки для перобразования текста из входного формата (учебный конфигурационный язык) в выходной (xml)
# Установка
Для начала, убедитесь, что у вас установлен Python. Затем выполните следующие шаги:
1.Установка программы и переход в директорию
```
git clone <URL репозитория>
cd <директория проекта>
```
2.Создайте и активируйте виртуальное окружение:
```
python3 -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate     # Для Windows
```
3.Установите необходимые зависимости (pytest для тестов)
```
pip install unittest
pip install lark
```
# Запуск скрипта
Скрипт принимает текст конфигурационного файла через стандартный ввод и выводит XML в файле.

Пример запуска:
```
python main.py --input input.txt --output output.xml
```
Здесь:
- input.txt — файл с конфигурационными данными на учебном языке.
- output.xml — файл, в который будет записан результат в формате xml.

# Примеры входных и выходных данных:
## Пример 1: Конфигурация параметров сервера
### Входные данные:
```
// Пример конфигурации
const PI = 3.14
const RADIUS = 10
const AREA = #{PI RADIUS RADIUS * *}

myArray = (list 1 2 3 4)

```
### Выходные данные (XML):
```
<?xml version="1.0" ?>
<configuration>
  <constant name="PI" value="3.14"/>
  <constant name="RADIUS" value="10.0"/>
  <constant name="AREA" value="314.0"/>
  <array name="myArray">
    <value>1.0</value>
    <value>2.0</value>
    <value>3.0</value>
    <value>4.0</value>
  </array>
</configuration>

```
# Тесты
Шаги запуска тестов:
1. Установить библиотеку unittest (необходимо, если не сделано ранее):
```
pip install unittest
```
2.Для запуска тестирования необходимо запустить следующий скрипт:
```
python -m unittest test.py
```
![изображение](https://github.com/user-attachments/assets/65eb7e09-a9ee-41fe-931a-27042260ef54)
