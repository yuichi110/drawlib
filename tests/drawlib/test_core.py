from drawlib.core import *


def test_circle():
    clear()
    config(width=10, height=10, axis=False)
    circle(5, 5, 3)
    save("test_circle.png")


def test_text():
    clear()
    config(width=10, height=10, axis=False)
    text(3, 3, "Hello World")
    save("test_text.png")


def test_line():
    clear()
    config(width=10, height=10, axis=True)
    line(2, 2, 5, 5)
    save("test_line.png")


def test_lines():
    clear()
    config(width=10, height=10, axis=True)
    lines([(1, 1), (2, 5), (3, 1)])
    save("test_lines.png")


def test_line_curved():
    clear()
    config(width=50, height=50, axis=True)
    points = [(0, 30, 0, 20, 10, 20), (20, 20), (30, 20, 30, 10), (30, 20, 40, 20)]
    line_bezier(points)
    save("test_line_bezier.png")
