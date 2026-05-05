import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from src import tokenize_code, render_code, render_terminal
from src.colors import PROMPT_USR, PROMPT_DIR, FG, CMD_COLOR, OUT_COLOR, INPUT_COLOR, RESULT_COLOR

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    examples_dir = Path(__file__).parent.parent / "examples"

    task1_code = read_file(examples_dir / "task1.cpp")
    task2_code = read_file(examples_dir / "task2.cpp")
    task3_code = read_file(examples_dir / "task3.cpp")

    task1_lines = tokenize_code(task1_code)
    task2_lines = tokenize_code(task2_code)
    task3_lines = tokenize_code(task3_code)

    render_code(task1_lines, "task1.cpp — Array1D: переміщення екстремумів", "code1.png", width=860)
    render_code(task2_lines, "task2.cpp — Array2D: суми негативних трикутників", "code2.png", width=900)
    render_code(task3_lines, "task3.cpp — Array1D: аналіз парних елементів", "code3.png", width=860)

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
    render_terminal(t1, "Тестування — Завдання 1: переміщення екстремумів", "test1.png")

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
    render_terminal(t2, "Тестування — Завдання 2: трикутні матриці", "test2.png", width=780)

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
    render_terminal(t3, "Тестування — Завдання 3: парні елементи", "test3.png")

    print("All screenshots done.")

if __name__ == "__main__":
    main()