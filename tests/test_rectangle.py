from drawlib import *
from drawlib.debug import get_function_name

FONT_FILE = "./assets/font.ttf"
OUTPUT_DIR = "../tests_output/rectangle/"


def test_rectangle():
    clear()
    config(width=10, height=10, grid=True)
    rectangle(3, 3, 5, 2, angle=45, text="Rectangle")
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_rectangle_style():
    clear()
    config(width=10, height=10, grid=True)
    rectangle(
        3,
        3,
        5,
        2,
        angle=45,
        text="Rectangle",
        style=ShapeStyle(
            lcolor="blue",
            fcolor="yellow",
            alpha=0.5,
            lstyle="dashed",
            lwidth=3,
        ),
    )
    save(f"{OUTPUT_DIR}{get_function_name()}.png")
