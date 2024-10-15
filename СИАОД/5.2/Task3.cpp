#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm> // Для std::sort

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
    size_t spacePos = record.find(' '); // Находим первое пробел
    return stoi(record.substr(0, spacePos)); // Преобразуем часть строки до первого пробела в число
}

// Функция для бинарного поиска по уникальному номеру
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

    // Бинарный поиск по уникальному номеру
    int left = 0;
    int right = records.size() - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        // Получение уникального номера из строки
        string record = records[mid];
        int number = extractNumber(record); // Извлекаем номер из строки

        if (number == targetNumber) {
            return record; // Нашли нужную запись
        }
        else if (number < targetNumber) {
            left = mid + 1;
        }
        else {
            right = mid - 1;
        }
    }

    return "Запись не найдена"; // Если запись не найдена
}

int main() {
    setlocale(LC_ALL, "rus");
    int targetNumber;
    cout << "Введите номер для поиска: ";
    cin >> targetNumber;
    clock_t t0 = clock();
    string result = binarySearchInFile("test.bin", targetNumber);
    cout << "Результат поиска: " << result << endl;
    clock_t t1 = clock();
    cout << "Время выполнения программы:  " << (double)(t1 - t0) / CLOCKS_PER_SEC << " секунд" << endl;
    return 0;
}
