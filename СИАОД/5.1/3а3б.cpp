#include <iostream>
#include <fstream>
#include <vector>
#include <ctime>
using namespace std;

const int MAX_NUM = 10000000;

int main() {
    setlocale(LC_ALL, "rus");
    int number_of_unique_numbers = 10000000;

    // размер битового массива: делим на 8, чтобы вместить биты в char
    vector<unsigned char> ArrayBit(MAX_NUM / 8, 0); // инициализация значениями 0
    size_t memoryUsage = ArrayBit.size() * sizeof(unsigned char);
    cout << "Объем оперативной памяти, занимаемый битовым массивом: " << memoryUsage << " байт." << endl;

    clock_t t0 = clock();

    ifstream inputFile("random_numbers.txt");
    if (!inputFile.is_open()) {
        cerr << "Ошибка открытия файла" << endl;
        return 1; // корректный выход при ошибке
    }

    int number;
    while (inputFile >> number) {
        if (number >= 0 && number < MAX_NUM) {
            // устанавливаем соответствующий бит в 1
            ArrayBit[number / 8] |= (1 << (number % 8)); // находим правильный байт и устанавливаем бит
        }
    }
    inputFile.close();

    ofstream outputFile("lolol.txt");
    if (!outputFile.is_open()) {
        cerr << "Ошибка открытия файла" << endl;
        return 1; // корректный выход при ошибке
    }

    // проходим по массиву и записываем индексы установленных битов в выходной файл
    for (int i = 0; i < MAX_NUM; ++i) {
        if (ArrayBit[i / 8] & (1 << (i % 8))) { // проверяем, установлен ли бит
            outputFile << i << endl; // запись уникального числа
        }
    }
    outputFile.close();

    clock_t t1 = clock();

    cout << "Числа из файла random_numbers.txt отсортированы и помещены в lolol.txt" << endl;
    cout << "Время выполнения программы:  " << (double)(t1 - t0) / CLOCKS_PER_SEC << " секунд" << endl;

    return 0; // корректное завершение программы
}
