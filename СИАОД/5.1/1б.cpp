#include <iostream>
using namespace std;
int main() {
	unsigned char x = 255;//8-разрядное двоичное число 11111111
	unsigned char maska = 1;//1=00000001 – 8-разрядная маска
	x = x & (maska << 6);//результат x = 64
	cout << (int)x;
	return 0;
}
