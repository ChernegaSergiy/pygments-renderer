import os
import glob
from PIL import Image, ImageDraw, ImageFont

DEFAULT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
DEFAULT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

FONT_SIZE = 15
PAD = 20
LINE_H = 22

_font_cache = {}

def find_system_font(font_name):
    if font_name in _font_cache:
        return _font_cache[font_name]

    search_dirs = [
        "/usr/share/fonts",
        "/usr/local/share/fonts",
        os.path.expanduser("~/.fonts"),
    ]

    if os.name == "nt":
        search_dirs.append(os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts"))
        font_name_lower = font_name.lower()
        for ext in [".ttf", ".ttc", ".otf"]:
            pattern = os.path.join(search_dirs[-1], f"*{ext}")
            for path in glob.glob(pattern):
                if font_name_lower in os.path.basename(path).lower():
                    _font_cache[font_name] = path
                    return path
    else:
        for base_dir in search_dirs:
            if not os.path.exists(base_dir):
                continue
            for ext in [".ttf", ".ttc", ".otf"]:
                pattern = os.path.join(base_dir, "**", f"*{ext}")
                for path in glob.glob(pattern, recursive=True):
                    basename = os.path.basename(path).lower()
                    if font_name.lower() in basename:
                        _font_cache[font_name] = path
                        return path

    return None

def load_font(size=FONT_SIZE, bold=False, font=None):
    path = None

    if font:
        if os.path.isfile(font):
            path = font
        else:
            path = find_system_font(font)

    if not path:
        path = DEFAULT_BOLD if bold else DEFAULT_MONO

    try:
        return ImageFont.truetype(path, size)
    except Exception:
        fallback = DEFAULT_BOLD if bold else DEFAULT_MONO
        return ImageFont.truetype(fallback, size)

def measure(text, font):
    dummy = Image.new("RGB", (1, 1))
    d = ImageDraw.Draw(dummy)
    bb = d.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]