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
