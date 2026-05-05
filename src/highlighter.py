from pygments import lex
from pygments.lexers import CppLexer, guess_lexer
from pygments.styles import get_style_by_name
from src import colors
from src.colors import FG

DEFAULT_TOKEN_COLORS = {
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

_token_colors = DEFAULT_TOKEN_COLORS

def load_theme(theme_name):
    global _token_colors
    if theme_name == "default":
        _token_colors = DEFAULT_TOKEN_COLORS
        return
    style = get_style_by_name(theme_name)
    token_colors = {}
    for token_type, style_def in style:
        color = style_def.get("color")
        if color:
            hex_color = color.lstrip("#")
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            token_str = str(token_type)
            if token_str.startswith("Token."):
                token_str = token_str[6:]
            token_colors[token_str] = rgb
    _token_colors = token_colors
    if style.background_color:
        hex_bg = style.background_color.lstrip("#")
        colors.BG = tuple(int(hex_bg[i:i+2], 16) for i in (0, 2, 4))

def get_token_color(token_type):
    token_str = str(token_type)
    if token_str.startswith("Token."):
        token_str = token_str[6:]
    for prefix, color in _token_colors.items():
        if token_str.startswith(prefix):
            return color
    parts = token_str.split(".")
    for i in range(len(parts)-1, 0, -1):
        prefix = ".".join(parts[:i])
        if prefix in _token_colors:
            return _token_colors[prefix]
    return FG

def tokenize_code(code_str, lexer=None):
    if lexer is None:
        return []
    tokens = list(lex(code_str, lexer))
    lines = code_str.split('\n')
    result = []
    token_idx = 0
    
    for line_idx, line in enumerate(lines, 1):
        parts = []
        line_len = len(line)
        pos = 0
        
        while token_idx < len(tokens):
            token_type, token_text = tokens[token_idx]
            
            if '\n' in token_text:
                parts_text = token_text.replace('\n', '')
                if parts_text:
                    parts.append((parts_text, get_token_color(token_type)))
                token_idx += 1
                break
            
            if pos >= line_len:
                break
                
            color = get_token_color(token_type)
            parts.append((token_text, color))
            pos += len(token_text)
            token_idx += 1
            
        if not parts:
            parts = [('', FG)]
        result.append((line_idx, parts))
        
    return result