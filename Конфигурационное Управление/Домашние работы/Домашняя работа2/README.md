## Описание
Эта программа строит граф зависимостей для коммитов, в узлах которого находятся списки файлов и папок. Граф необходимо строить только для тех коммитов, где фигурирует файл с заданным именем. Зависимости определяются для git-репозитория. Для описания графа зависимостей используется представление Graphviz. Визуализатор выводит результат на экран в виде кода
## Установка
1.Установка программы и переход в директорию
```
git clone <URL репозитория>
cd <директория проекта>
```
2.Вывести в виде графа, имея сгенерированный код в формате Graphviz, можно на https://dreampuf.github.io/GraphvizOnline/#

3.Убедитесь, что у вас установлен python

4.Создайте и активируйте виртуальное окружение
```
python3 -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate     # Для Windows
```
5.Установите необходимые зависимости для тестов
```
pip install unittest
```
## Запуск визуализат
Выполнить следующую команду
```
python main.py --graphviz-path "C:\Program Files\Graphviz\bin\dot.exe" --repo-path "D:\test-repo"  --output-path "C:\Users\Mi\Desktop\lala.dot" --filename "file1.txt"
```
## Выходные данные
Программа сгененерирует код в формате Graphviz
## Пример
![изображение](https://github.com/user-attachments/assets/b8c321ab-c784-43b2-a06e-4b8452a03fdc)
![изображение](https://github.com/user-attachments/assets/3bd88abc-8211-4e28-bdd3-50b63cb38eaa)

## Тесты
```
python -m unittest test.py
```
![изображение](https://github.com/user-attachments/assets/81f69cef-fb55-4e8a-aad9-24a6a16c16f8)
