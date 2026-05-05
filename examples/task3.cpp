#include <iostream>
using namespace std;

bool isEven(int val) { return val % 2 == 0; }

class Array1D {
    int* data;
    int size;
public:
    void allocate(int n) { size = n; data = new int[size]; }
    void release() { delete[] data; }
    void readFromInput() {
        cout << "Введіть " << size << " елементів:\\n";
        for (int i = 0; i < size; i++) {
            cout << "data[" << i << "] = ";
            cin >> data[i];
        }
    }
    void analyzeEvenElements() {
        int sum = 0, count = 0;
        for (int i = 0; i < size; i++)
            if (isEven(data[i])) { sum += data[i]; count++; }
        double avg = count > 0 ? (double)sum / count : 0.0;
        cout << "Кількість парних елементів: " << count << "\\n";
        cout << "Сума парних елементів: " << sum << "\\n";
        cout << "Середнє арифметичне: " << avg << "\\n";
    }
};

int main() {
    Array1D obj;
    int n;
    cout << "Розмір масиву: ";
    cin >> n;
    obj.allocate(n);
    obj.readFromInput();
    obj.analyzeEvenElements();
    obj.release();
    return 0;
}