from drawlib import *
import inspect

FONT_FILE = "tests_input/font.ttf"
OUTPUT_DIR = "tests_output/rectangle_rounded/"


def test_rectangle_rounded():
    clear()
    config(width=10, height=10, grid=True)
    rectangle_rounded(3, 3, 5, 2, text="Rounded\nRectangle")
    save(f"{OUTPUT_DIR}{inspect.stack()[0][3]}.png")


def test_rectangle_rounded_rotate():
    clear()
    config(width=10, height=10, grid=True)
    rectangle_rounded(
        3,
        3,
        5,
        2,
        angle=-90,
        text="Rounded\nRectangle",
        style=ShapeStyle(
            lcolor="blue",
            fcolor="yellow",
            alpha=0.5,
            lstyle="dashed",
            lwidth=3,
        ),
    )
    save(f"{OUTPUT_DIR}{inspect.stack()[0][3]}.png")
