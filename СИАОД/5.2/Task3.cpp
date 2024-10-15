#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm> // Для std::sort
#include <cmath>     // Для std::floor

using namespace std;

// Функция для чтения строки из бинарного файла
string readString(ifstream& binFile) {
    size_t length;
    binFile.read(reinterpret_cast<char*>(&length), sizeof(length)); // Читаем длину строки
    string line(length, ' ');
    binFile.read(&line[0], length); // Читаем строку
    return line;
}

// Функция для извлечения уникального номера из строки
int extractNumber(const string& record) {
    size_t spacePos = record.find(' '); // Находим первый пробел
    return stoi(record.substr(0, spacePos)); // Преобразуем часть строки до первого пробела в число
}

// Функция для поиска по уникальному номеру с использованием середины и шага
string searchWithMidAndStep(const vector<string>& records, int targetNumber) {
    int size = records.size();
    int mid = size / 2;  // Начинаем с середины
    int step = mid / 2;  // Шаг будет уменьшаться на каждом шаге

    while (step > 0) {
        int number = extractNumber(records[mid]);  // Получаем номер из середины

        if (number == targetNumber) {
            return records[mid];  // Нашли нужную запись
        }
        else if (number < targetNumber) {
            mid += step;  // Двигаемся вправо
        }
        else {
            mid -= step;  // Двигаемся влево
        }

        step = step / 2;  // Уменьшаем шаг вдвое
    }

    // Находимся между двумя соседними элементами, проверяем оба
    if (extractNumber(records[mid]) == targetNumber) {
        return records[mid];  // Нашли нужную запись
    }
    if (mid + 1 < size && extractNumber(records[mid + 1]) == targetNumber) {
        return records[mid + 1];  // Проверяем следующий элемент
    }

    return "Запись не найдена";  // Если запись не найдена
}

string binarySearchInFile(const string& filename, int targetNumber) {
    ifstream binFile(filename, ios::binary);

    if (!binFile) {
        cerr << "Не удалось открыть бинарный файл!" << endl;
        return "";
    }

    // Считывание всех строк из файла
    vector<string> records;
    while (binFile.peek() != EOF) {
        records.push_back(readString(binFile));
    }

    binFile.close();

    // Сортировка строк по уникальному номеру
    sort(records.begin(), records.end(), [](const string& a, const string& b) {
        return extractNumber(a) < extractNumber(b);
        });

    // Поиск по уникальному номеру с использованием середины и шага
    return searchWithMidAndStep(records, targetNumber);
}

int main() {
    setlocale(LC_ALL, "rus");
    int targetNumber;
    cout << "Введите номер для поиска: ";
    cin >> targetNumber;

    string result = binarySearchInFile("test.bin", targetNumber);
    cout << "Результат поиска: " << result << endl;

    return 0;
}
