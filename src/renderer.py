from PIL import Image, ImageDraw
import src.colors
from src.fonts import load_font, measure, FONT_SIZE, PAD, LINE_H

def titlebar(draw, width, title, font):
    draw.rectangle([(0,0),(width,28)], fill=(37,37,38))
    draw.text((PAD, 6), title, font=font, fill=(150,150,150))
    for i, col in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        cx = width - 20 - i*18
        draw.ellipse([(cx-5,8),(cx+5,18)], fill=col)

def render_code(lines_with_colors, title, output_path, width=880, start_line=1, font_name=None):
    font = load_font(font=font_name)
    title_font = load_font(13, font=font_name)
    height = PAD*2 + 30 + len(lines_with_colors)*LINE_H + PAD
    img = Image.new("RGB", (width, height), src.colors.BG)
    draw = ImageDraw.Draw(img)
    titlebar(draw, width, title, title_font)
    y = 28 + PAD
    current_line = start_line
    for linenum, parts in lines_with_colors:
        x = PAD
        num_str = f"{current_line:3d}  "
        draw.text((x, y), num_str, font=font, fill=(80,80,80))
        x += measure(num_str, font)
        for text, color in parts:
            draw.text((x, y), text, font=font, fill=color)
            x += measure(text, font)
        y += LINE_H
        current_line += 1
    img.save(output_path)
    print(f"Saved: {output_path}")

def render_terminal(lines, title, output_path, width=740):
    font = load_font()
    title_font = load_font(13)
    height = PAD*2 + 30 + len(lines)*LINE_H + PAD
    img = Image.new("RGB", (width, height), src.colors.TERM_BG)
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