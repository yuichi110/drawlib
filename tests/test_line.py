from drawlib import *
from drawlib.debug import get_function_name

OUTPUT_DIR = "../tests_output/line/"


def test_line():
    clear()
    config(width=10, height=10, grid=True)
    line(2, 2, 5, 5)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_line_style():
    clear()
    config(width=10, height=10, grid=True)
    style = LineStyle(width=3, color="red", style="dotted", alpha=0.5)
    line(2, 2, 5, 5, style)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_lines():
    clear()
    config(width=10, height=10, grid=True)
    lines([(1, 1), (2, 5), (3, 1)])
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_line_bezier():
    clear()
    config(width=50, height=50, grid=True)
    points = [(0, 20, 10, 20), (20, 20), (30, 20, 30, 10), (30, 20, 40, 20)]
    line_bezier(0, 30, points)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")
