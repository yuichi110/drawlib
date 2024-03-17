from drawlib.core import *
from PIL import Image, ImageFilter


def test_circle():
    clear()
    config(width=10, height=10, axis=False)
    circle(5, 5, 3)
    save("test_circle.png")


def test_title():
    clear()
    config(width=10, height=10, axis=True)
    title("Test Title", y=-0.1)
    save("test_title.png")


def test_title_font():
    clear()
    config(width=10, height=10, axis=True)
    style = FontStyle(file="test-font.ttf")
    title("タイトルのテスト", y=-0.1, style=style)
    save("test_title_font.png")


def test_text():
    clear()
    config(width=10, height=10, axis=False)
    text(3, 3, "Hello World")
    save("test_text.png")


def test_text_font():
    warning_suppress()
    clear()
    config(width=10, height=10, axis=False)
    text(3, 3, "あいうえお")
    style = FontStyle(file="test-font.ttf")
    text(6, 6, "あいうえお", style=style)
    save("test_text_font.png")


def test_image_file():
    clear()
    config(width=10, height=10, axis=True)
    image(1, 1, "test-icon.png", zoom=0.1)
    save("test_image_file.png")


def test_image_pil():
    clear()
    config(width=10, height=10, axis=True)
    im = Image.open("test-icon.png")
    image(1, 1, pilimg=im, zoom=0.1)
    save("test_image_pil.png")


def test_line():
    clear()
    config(width=10, height=10, axis=True)
    line(2, 2, 5, 5)
    save("test_line.png")


def test_line_style():
    clear()
    config(width=10, height=10, axis=True)
    style = LineStyle(width=3, color="red", style="dotted", alpha=0.5)
    line(2, 2, 5, 5, style)
    save("test_line_style.png")


def test_lines():
    clear()
    config(width=10, height=10, axis=True)
    lines([(1, 1), (2, 5), (3, 1)])
    save("test_lines.png")


def test_line_bezier():
    clear()
    config(width=50, height=50, axis=True)
    points = [(0, 20, 10, 20), (20, 20), (30, 20, 30, 10), (30, 20, 40, 20)]
    line_bezier(0, 30, points)
    save("test_line_bezier.png")
