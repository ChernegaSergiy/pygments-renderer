from PIL import Image, ImageDraw, ImageFont

MONO_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

FONT_SIZE = 15
PAD = 20
LINE_H = 22

def load_font(size=FONT_SIZE, bold=False):
    path = MONO_BOLD if bold else MONO_FONT
    return ImageFont.truetype(path, size)

def measure(text, font):
    dummy = Image.new("RGB", (1, 1))
    d = ImageDraw.Draw(dummy)
    bb = d.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]