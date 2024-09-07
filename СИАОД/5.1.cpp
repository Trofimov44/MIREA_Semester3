Задание 1а:
int main() {
  unsigned char x = 255;
  unsigned char maska = 1;
  x = x & (~(maska << 4));
  cout << (int)x;
  return 0;
}

Задание 1б:
int main() {
  unsigned char x = 255;
  unsigned char maska = 1;
  x = x & (maska << 6);
  cout << (int)x;
  return 0;
}

Задание 1в:
#include <cstdlib>
#include <iostream>
#include <Windows.h>
#include <bitset>
using namespace std;
int main()
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    unsigned int x = 25;
    const int n = sizeof(int) * 8; //=32 - количество разрядов в числе типа int
    unsigned maska = (1 << n - 1); //1 в старшем бите 32-разрядной сетки
    cout << "Начальный вид маски: " << bitset<n>(maska) << endl;
    cout << "Результат: ";
    for (int i = 1; i <= n; i++) //32 раза - по количеству разрядов:
    {
        cout << ((x & maska) >> (n - i));
        maska = maska >> 1; //смещение 1 в маске на разряд вправо
    }

    cout << endl;
    system("pause");
    return 0;
}


Задание 2а:
#include <iostream>
using namespace std;

int main()
{
    int arr[] = {1, 0, 5, 7, 2, 4};

    unsigned char maska = 1;
    unsigned char ArrayBit = 0;

    for (int i: arr) {
        ArrayBit = ArrayBit | (maska << i);
    }
    
    for (int i = 0; i < 8; i++) {
        if (ArrayBit & (maska << i)) {
            cout << i << " ";
        }
    }
    
    return 0;
}

Задание 2б:
#include <iostream>
using namespace std;

int main()
{
    int arr[] = {1, 2, 63};

    unsigned long long maska = 1;
    unsigned long long ArrayBit = 0;

    for (int i: arr) {
        ArrayBit = ArrayBit | (maska << i);
    }
    
    for (int i = 0; i < 64; i++) {
        if (ArrayBit & (maska << i)) {
            cout << i << " ";
        }
    }
    
    return 0;
}

Задание 2в:
#include <iostream>
#include <vector>
using namespace std;

int main()
{
    int arr[] = {1, 4, 34, 2 };

    vector<unsigned char> ArrayBits{0, 0, 0, 0, 0, 0, 0, 0};  // 8 байтов для представления 64 бит
    unsigned char maska = 1;

    // Установка битов
    for (int i : arr) {
        ArrayBits[i / 8] = ArrayBits[i / 8] | (maska << (i % 8));  // Устанавливаем бит в нужном байте и позиции
    }

    // Проверка битов и вывод чисел
    for (int i = 0; i < 64; i++) {
        if (ArrayBits[i / 8] & (maska << (i % 8))) {
            cout << i << " ";
        }
    }

    return 0;
}

Задание 3a:
#include <iostream>
#include <fstream>
#include <vector>
#include <ctime>
using namespace std;

const int MAX_NUM = 10000000;

int main() {
    setlocale(LC_ALL, "rus");
    // Засекаем время начала программы
    clock_t t0 = clock();

    // Создаем битовый массив, представленный в виде массива целых чисел
    vector<bool> ArrayBit(MAX_NUM, 0);

    // Открываем файл для чтения
    ifstream inputFile("lalala.txt");
    if (!inputFile.is_open()) {
        cerr << "Ошибка открытия файла " << endl;
        return 1;
    }

    // Читаем числа из файла и выставляем соответствующие биты
    int number;
    while (inputFile >> number) {
        if (number >= 0 && number < MAX_NUM) {
            ArrayBit[number] = 1;
        }
    }

    inputFile.close();  // Закрываем файл

    // Открываем файл для записи
    ofstream outputFile("lolol.txt");
    if (!outputFile.is_open()) {
        cerr << "Ошибка открытия файла" << endl;
        return 1;
    }

    // Проходим по битовому массиву и записываем индексы установленных битов в выходной файл
    for (int i = 0; i < MAX_NUM; ++i) {
        if (ArrayBit[i]) {
            outputFile << i << endl;
        }
    }

    outputFile.close();  // Закрываем файл

    // Засекаем время окончания программы
    clock_t t1 = clock();

    // Выводим время выполнения программы
    cout << "Числа из файла lalal.txt отсортированы и помещены в lolol.txt Время выполнения программы: " << (double)(t1 - t0) / CLOCKS_PER_SEC << " секунд" << endl;

    return 0;
}
