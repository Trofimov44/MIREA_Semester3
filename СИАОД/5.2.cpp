#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <ctime>
#include <unordered_set>
#include <vector>

using namespace std;

// ЗАДАНИЕ 1
int task1() {
    // Массивы для данных
    string Destination[5] = {
        "Новгород Великий",
        "Новгород Нижний",
        "Санкт-Петербург",
        "Владивосток",
        "Новосибирск"
    };
    string Departure[5] = {
        "Смоленск",
        "Москва",
        "Волгоград",
        "Вятка",
        "Самара"
    };

    int count = 10;
    int Number;
    vector<int> sp(1000000, 1);  // Вектор для генерации уникальных номеров

    // Создание текстового файла
    ofstream outFile("test.txt");
    if (!outFile) {
        cerr << "Не удалось создать файл lolol.txt!" << endl;
        exit(0);
    }

    // Запись данных в текстовый файл
    while (count != 0) {
        Number = 10000 + rand() % 90000; // Генерация уникального номера
        if (sp[Number] == 1) {
            outFile << Number << " " << Departure[rand() % 5] << " " << Destination[(rand() % 5)] << " " << rand() % 24 << ":" << rand() % 59 + 10 << endl;
            count = count - 1;
            sp[Number] = 0; // Отметка, что номер использован
        }
    }

    outFile.close(); // Закрытие текстового файла
    cout << "Текстовый файл успешно создан" << endl;

    // Чтение данных из текстового файла и запись в двоичный файл
    ifstream inFile("test.txt");   // Открытие текстового файла для чтения
    ofstream binFile("test.bin", ios::binary); // Открытие двоичного файла для записи

    string line;
    while (getline(inFile, line)) {
        size_t length = line.size();
        binFile.write(reinterpret_cast<char*>(&length), sizeof(length)); // Запись длины строки
        binFile.write(line.c_str(), length); // Запись самой строки
    }

    inFile.close();  // Закрытие текстового файла
    binFile.close(); // Закрытие двоичного файла

    cout << "Двоичный файл успешно создан" << endl;
    return 0;
}

// ЗАДАНИЕ 2
int task2() {
    // Открываем двоичный файл для чтения
    ifstream binFile("test.bin", ios::binary);
    if (!binFile) {
        cerr << "Не удалось открыть двоичный файл!" << endl;
        exit(0);
    }

    // Ввод ключа для поиска
    string searchKey;
    cout << "Введите номер для поиска: ";
    cin >> searchKey;
    clock_t t0 = clock();
    size_t length;
    bool found = false;

    // Линейный поиск по двоичному файлу
    while (binFile.read(reinterpret_cast<char*>(&length), sizeof(length))) {
        string line(length, '\0');  // Создаем строку нужной длины
        binFile.read(&line[0], length);  // Считываем строку из двоичного файла

        // Проверка, начинается ли строка с искомого ключа
        if (line.substr(0, searchKey.size()) == searchKey) {
            cout << "Найдена запись: " << line << endl;
            found = true;
            break;
        }
    }
    clock_t t1 = clock();
    if (!found) {
        cout << "Запись с номером " << searchKey << " не найдена." << endl;
    }

    binFile.close();  // Закрываем двоичный файл
    cout << "Время выполнения программы:  " << (double)(t1 - t0) / CLOCKS_PER_SEC << " секунд" << endl; \
    return 0;
}

// ЗАДАНИЕ 3
int task3(){
    return 0;
}

int main() {
    int a;
    setlocale(LC_ALL, "rus");
    cout << "Введите номер задания: ";
    cin >> a;

    switch (a){
        case 1:
            task1();
            break;
        case 2:
            task2();
            break;
        default:
            cout << "Такого задание нет";
            break;
    }

    return 0;
}   
