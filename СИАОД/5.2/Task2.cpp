#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace std;


int main() {
    setlocale(LC_ALL, "rus");
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
