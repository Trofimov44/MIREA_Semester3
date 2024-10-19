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
