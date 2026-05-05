#include <iostream>
using namespace std;

class Array2D {
    int** data;
    int rows, cols;
public:
    void allocate(int r, int c) {
        rows = r; cols = c;
        data = new int*[rows];
        for (int i = 0; i < rows; i++)
            data[i] = new int[cols];
    }
    void release() {
        for (int i = 0; i < rows; i++) delete[] data[i];
        delete[] data;
    }
    void readFromInput() {
        for (int i = 0; i < rows; i++)
            for (int j = 0; j < cols; j++) {
                cout << "data[" << i << "][" << j << "] = ";
                cin >> data[i][j];
            }
    }
    void print() {
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++)
                cout << data[i][j] << "\\t";
            cout << "\\n";
        }
    }
    void sumNegativeTriangles() {
        int sumUpper = 0, sumLower = 0;
        for (int i = 0; i < rows; i++)
            for (int j = 0; j < cols; j++) {
                if (i <= j && data[i][j] < 0) sumUpper += data[i][j];
                if (i >= j && data[i][j] < 0) sumLower += data[i][j];
            }
        int* result = new int[2];
        result[0] = sumUpper;  result[1] = sumLower;
        cout << "Новий масив [Верхня, Нижня]: [" << result[0] << ", " << result[1] << "]\\n";
        delete[] result;
    }
};

int main() {
    Array2D obj;
    int r, c;
    cout << "Введіть кількість рядків і стовпців: ";
    cin >> r >> c;
    obj.allocate(r, c);
    obj.readFromInput();
    cout << "Двовимірний масив:\\n";
    obj.print();
    obj.sumNegativeTriangles();
    obj.release();
    return 0;
}