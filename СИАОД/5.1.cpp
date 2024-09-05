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
        if (ArrayBit & (1 << i)) {
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
