#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace std;


int main() {
    setlocale(LC_ALL, "rus");
    // Массивы для данных
    string Destination[5] = { "Новгород Великий","Новгород Нижний","Санкт-Петербург",
                            "Владивосток","Новосибирск"};
    string Departure[5] = {
        "Смоленск","Москва","Волгоград",
        "Вятка","Самара"
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
            outFile << Number << " " << Departure[rand() % 5] << " " << Destination[(rand() % 5)]
                << " " << rand() % 24 << ":" << rand() % 59 + 10 << endl;
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
