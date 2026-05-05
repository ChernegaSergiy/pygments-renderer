from PIL import Image, ImageDraw, ImageFont
from pygments import lex
from pygments.lexers import CppLexer
from pygments.styles import get_style_by_name

MONO_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

BG = (30, 30, 30)
FG = (212, 212, 212)

TERM_BG = (12, 12, 12)
TERM_FG = (204, 204, 204)
PROMPT_USR = (87, 187, 138)
PROMPT_DIR = (100, 160, 220)
CMD_COLOR = (255, 255, 255)
OUT_COLOR = (204, 204, 204)
INPUT_COLOR = (255, 230, 100)
RESULT_COLOR = (120, 220, 120)

FONT_SIZE = 15
PAD = 20
LINE_H = 22

DEFAULT_STYLE = get_style_by_name("monokai")

TOKEN_COLORS = {
    "Keyword": (86, 156, 214),
    "Keyword.Constant": (86, 156, 214),
    "Keyword.Declaration": (86, 156, 214),
    "Keyword.Namespace": (255, 100, 130),
    "Keyword.Pseudo": (86, 156, 214),
    "Keyword.Reserved": (86, 156, 214),
    "Keyword.Type": (78, 201, 176),
    "Name": FG,
    "Name.Class": (220, 220, 170),
    "Name.Function": (220, 220, 170),
    "Name.Variable": FG,
    "Name.Builtin": (220, 220, 170),
    "Literal": (181, 206, 168),
    "Literal.Number": (181, 206, 168),
    "Literal.String": (206, 145, 120),
    "Comment": (106, 153, 85),
    "Operator": (255, 100, 130),
    "Punctuation": FG,
    "Generic": FG,
}

def get_token_color(token_type):
    token_str = str(token_type)
    if token_str.startswith("Token."):
        token_str = token_str[6:]
    for prefix, color in TOKEN_COLORS.items():
        if token_str.startswith(prefix):
            return color
    return FG

def hex_to_rgb(hex_color):
    if hex_color is None:
        return None
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def load_font(size=FONT_SIZE, bold=False):
    path = MONO_BOLD if bold else MONO_FONT
    return ImageFont.truetype(path, size)

def measure(text, font):
    dummy = Image.new("RGB", (1, 1))
    d = ImageDraw.Draw(dummy)
    bb = d.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]

def titlebar(draw, width, title, font):
    draw.rectangle([(0,0),(width,28)], fill=(37,37,38))
    draw.text((PAD, 6), title, font=font, fill=(150,150,150))
    for i, col in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        cx = width - 20 - i*18
        draw.ellipse([(cx-5,8),(cx+5,18)], fill=col)

def tokenize_code(code_str, lexer=None):
    if lexer is None:
        lexer = CppLexer()
    lines = code_str.split('\n')
    result = []
    for i, line in enumerate(lines, 1):
        tokens = list(lex(line, lexer))
        parts = []
        for token_type, token_text in tokens:
            if token_text:
                color = get_token_color(token_type)
                parts.append((token_text, color))
        if not parts:
            parts = [('', FG)]
        result.append((i, parts))
    return result

def render_code(lines_with_colors, title, output_path, width=880):
    font = load_font()
    title_font = load_font(13)
    height = PAD*2 + 30 + len(lines_with_colors)*LINE_H + PAD
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)
    titlebar(draw, width, title, title_font)
    y = 28 + PAD
    for linenum, parts in lines_with_colors:
        x = PAD
        num_str = f"{linenum:3d}  "
        draw.text((x, y), num_str, font=font, fill=(80,80,80))
        x += measure(num_str, font)
        for text, color in parts:
            draw.text((x, y), text, font=font, fill=color)
            x += measure(text, font)
        y += LINE_H
    img.save(output_path)
    print(f"Saved: {output_path}")

def render_terminal(lines, title, output_path, width=740):
    font = load_font()
    title_font = load_font(13)
    height = PAD*2 + 30 + len(lines)*LINE_H + PAD
    img = Image.new("RGB", (width, height), TERM_BG)
    draw = ImageDraw.Draw(img)
    titlebar(draw, width, title, title_font)
    y = 28 + PAD
    for parts in lines:
        x = PAD
        for text, color in parts:
            draw.text((x, y), text, font=font, fill=color)
            x += measure(text, font)
        y += LINE_H
    img.save(output_path)
    print(f"Saved: {output_path}")

def c(text, color=FG):
    return (text, color)

task1_code = '''#include <iostream>
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
}'''

task2_code = '''#include <iostream>
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
        cout << "Новий масив [Верхня, Нижка]: [" << result[0] << ", " << result[1] << "]\\n";
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
}'''

task3_code = '''#include <iostream>
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
}'''

lexer = CppLexer()
task1_lines = tokenize_code(task1_code, lexer)
task2_lines = tokenize_code(task2_code, lexer)
task3_lines = tokenize_code(task3_code, lexer)

render_code(task1_lines, "task1.cpp — Array1D: переміщення екстремумів", "/home/victus/code1.png", width=860)
render_code(task2_lines, "task2.cpp — Array2D: суми негативних трикутників", "/home/victus/code2.png", width=900)
render_code(task3_lines, "task3.cpp — Array1D: аналіз парних елементів", "/home/victus/code3.png", width=860)

USR = PROMPT_USR
DIR = PROMPT_DIR

t1 = [
    [("victus@DESKTOP-GUK7A21", USR), (":", FG), ("~/lab6", DIR), ("$ ", FG), ("./task1", CMD_COLOR)],
    [("Розмір масиву: ", OUT_COLOR), ("7", INPUT_COLOR)],
    [("Введіть 7 елементів:", OUT_COLOR)],
    [("data[0] = ", OUT_COLOR), ("3", INPUT_COLOR)],
    [("data[1] = ", OUT_COLOR), ("-5", INPUT_COLOR)],
    [("data[2] = ", OUT_COLOR), ("8", INPUT_COLOR)],
    [("data[3] = ", OUT_COLOR), ("1", INPUT_COLOR)],
    [("data[4] = ", OUT_COLOR), ("-2", INPUT_COLOR)],
    [("data[5] = ", OUT_COLOR), ("7", INPUT_COLOR)],
    [("data[6] = ", OUT_COLOR), ("4", INPUT_COLOR)],
    [("До перетворення:    ", OUT_COLOR), ("3 -5 8 1 -2 7 4", CMD_COLOR)],
    [("Після перетворення: ", OUT_COLOR), ("-5 3 4 1 -2 7 8", RESULT_COLOR)],
    [("victus@DESKTOP-GUK7A21", USR), (":", FG), ("~/lab6", DIR), ("$ ", FG)],
]
render_terminal(t1, "Тестування — Завдання 1: переміщення екстремумів", "/home/victus/test1.png")

t2 = [
    [("victus@DESKTOP-GUK7A21", USR), (":", FG), ("~/lab6", DIR), ("$ ", FG), ("./task2", CMD_COLOR)],
    [("Введіть кількість рядків і стовпців: ", OUT_COLOR), ("3 3", INPUT_COLOR)],
    [("data[0][0] = ", OUT_COLOR), ("2", INPUT_COLOR)],
    [("data[0][1] = ", OUT_COLOR), ("-3", INPUT_COLOR)],
    [("data[0][2] = ", OUT_COLOR), ("5", INPUT_COLOR)],
    [("data[1][0] = ", OUT_COLOR), ("-1", INPUT_COLOR)],
    [("data[1][1] = ", OUT_COLOR), ("4", INPUT_COLOR)],
    [("data[1][2] = ", OUT_COLOR), ("-6", INPUT_COLOR)],
    [("data[2][0] = ", OUT_COLOR), ("3", INPUT_COLOR)],
    [("data[2][1] = ", OUT_COLOR), ("-2", INPUT_COLOR)],
    [("data[2][2] = ", OUT_COLOR), ("1", INPUT_COLOR)],
    [("Двовимірний масив:", OUT_COLOR)],
    [("2\t-3\t5", CMD_COLOR)],
    [("-1\t4\t-6", CMD_COLOR)],
    [("3\t-2\t1", CMD_COLOR)],
    [("Новий масив [Верхня, Нижня]: ", OUT_COLOR), ("[-9, -3]", RESULT_COLOR)],
    [("victus@DESKTOP-GUK7A21", USR), (":", FG), ("~/lab6", DIR), ("$ ", FG)],
]
render_terminal(t2, "Тестування — Завдання 2: трикутні матриці", "/home/victus/test2.png", width=780)

t3 = [
    [("victus@DESKTOP-GUK7A21", USR), (":", FG), ("~/lab6", DIR), ("$ ", FG), ("./task3", CMD_COLOR)],
    [("Розмір масиву: ", OUT_COLOR), ("8", INPUT_COLOR)],
    [("Введіть 8 елементів:", OUT_COLOR)],
    [("data[0] = ", OUT_COLOR), ("1", INPUT_COLOR)],
    [("data[1] = ", OUT_COLOR), ("4", INPUT_COLOR)],
    [("data[2] = ", OUT_COLOR), ("-3", INPUT_COLOR)],
    [("data[3] = ", OUT_COLOR), ("6", INPUT_COLOR)],
    [("data[4] = ", OUT_COLOR), ("-8", INPUT_COLOR)],
    [("data[5] = ", OUT_COLOR), ("2", INPUT_COLOR)],
    [("data[6] = ", OUT_COLOR), ("5", INPUT_COLOR)],
    [("data[7] = ", OUT_COLOR), ("10", INPUT_COLOR)],
    [("Кількість парних елементів: ", OUT_COLOR), ("5", RESULT_COLOR)],
    [("Сума парних елементів: ",       OUT_COLOR), ("14", RESULT_COLOR)],
    [("Середнє арифметичне: ",         OUT_COLOR), ("2.8", RESULT_COLOR)],
    [("victus@DESKTOP-GUK7A21", USR), (":", FG), ("~/lab6", DIR), ("$ ", FG)],
]
render_terminal(t3, "Тестування — Завдання 3: парні елементи", "/home/victus/test3.png")

print("All screenshots done.")