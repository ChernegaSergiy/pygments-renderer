#include <iostream>
using namespace std;

class Array1D {
    int* data;
    int size;
public:
    void allocate(int n) {
        size = n;
        data = new int[size];
    }
    void release() { delete[] data; }
    void readFromInput() {
        cout << "Введіть " << size << " елементів:\\n";
        for (int i = 0; i < size; i++) {
            cout << "data[" << i << "] = ";
            cin >> data[i];
        }
    }
    void print() {
        for (int i = 0; i < size; i++)
            cout << data[i] << " ";
        cout << "\\n";
    }
    void moveExtremaToEnds() {
        if (size < 2) return;
        int minIdx = 0, maxIdx = 0;
        for (int i = 1; i < size; i++) {
            if (data[i] < data[minIdx]) minIdx = i;
            if (data[i] > data[maxIdx]) maxIdx = i;
        }
        if (minIdx == size - 1) minIdx = maxIdx;
        int temp = data[maxIdx];
        data[maxIdx] = data[size - 1];
        data[size - 1] = temp;
        temp = data[minIdx];
        data[minIdx] = data[0];
        data[0] = temp;
    }
};

int main() {
    Array1D obj;
    int n;
    cout << "Розмір масиву: ";
    cin >> n;
    obj.allocate(n);
    obj.readFromInput();
    cout << "До перетворення: ";
    obj.print();
    obj.moveExtremaToEnds();
    cout << "Після перетворення: ";
    obj.print();
    obj.release();
    return 0;
}