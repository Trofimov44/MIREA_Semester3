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
    size_t spacePos = record.find(' '); // Находим первый пробел
    return stoi(record.substr(0, spacePos)); // Преобразуем часть строки до первого пробела в число
}

// Функция для поиска по уникальному номеру с использованием середины и шага
string searchWithMidAndStep(const vector<string>& records, int targetNumber) {
    int size = records.size();
    int mid = size / 2;  // Начинаем с середины
    int step = mid / 2;  // Начальный шаг - половина середины
    int iterationCount = 0;  // Счётчик итераций

    while (step >= 1 && iterationCount < 800) {  // Ограничение на 500 итераций
        int number = extractNumber(records[mid]);  // Получаем номер из середины

        if (number == targetNumber) {
            return records[mid];  // Нашли нужную запись
        }
        else if (number < targetNumber) {
            mid = min(mid + step, size - 1);  // Двигаемся вправо, не выходя за пределы
        }
        else {
            mid = max(mid - step, 0);  // Двигаемся влево, не выходя за пределы
        }

        step = max(step / 2, 1);  // Минимальный шаг должен быть 1
        iterationCount++;  // Увеличиваем счётчик итераций
    }

    // Проверка всех возможных соседних элементов, если шаг 1 не сработал
    for (int i = max(mid - 1, 0); i <= min(mid + 1, size - 1); ++i) {
        if (extractNumber(records[i]) == targetNumber) {
            return records[i];  // Нашли нужную запись
        }
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
    int targetNumber;
    cout << "Введите номер для поиска: ";
    cin >> targetNumber;
    clock_t t0 = clock();
    string result = binarySearchInFile("test.bin", targetNumber);
    clock_t t1 = clock();
    cout << "Результат поиска: " << result << endl;
    cout << "Время выполнения программы:  " << (double)(t1 - t0) / CLOCKS_PER_SEC << " секунд" << endl;
    return 0;
}
