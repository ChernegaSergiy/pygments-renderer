import argparse
from pathlib import Path

from pygments.lexers import get_lexer_by_name

from src import tokenize_code, load_theme, render_code, render_terminal


def main():
    parser = argparse.ArgumentParser(description="Generate syntax-highlighted code screenshots")
    parser.add_argument("input", help="Input file path")
    parser.add_argument("-o", "--output", default="output.png", help="Output image path (default: output.png)")
    parser.add_argument("-l", "--language", help="Language (e.g., cpp, python, html, html+php)")
    parser.add_argument("-t", "--theme", default="default", help="Color theme (default, monokai, dracula, etc.)")
    parser.add_argument("-w", "--width", type=int, default=880, help="Image width (default: 880)")
    parser.add_argument("-T", "--title", help="Window title")
    args = parser.parse_args()

    if args.theme != "default":
        load_theme(args.theme)

    lexer = None
    if args.language:
        lexer = get_lexer_by_name(args.language)

    with open(args.input, 'r', encoding='utf-8') as f:
        code = f.read()

    lines = tokenize_code(code, lexer)

    title = args.title or Path(args.input).name
    render_code(lines, title, args.output, args.width)

    print(f"Generated: {args.output}")


if __name__ == "__main__":
    main()