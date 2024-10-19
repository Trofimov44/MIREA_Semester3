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
