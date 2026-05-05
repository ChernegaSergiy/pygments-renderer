from pygments import lex
from pygments.lexers import CppLexer
from src.colors import FG

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