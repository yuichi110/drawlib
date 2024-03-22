from drawlib import *

FONT_FILE = "tests_input/font.ttf"
OUTPUT_DIR = "tests_output/circle/"


def test_circle():
    clear()
    config(width=10, height=10, grid=True)
    circle(5, 5, 3)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_circle_text():
    clear()
    config(width=10, height=10, grid=True)
    circle(5, 5, 3, text="Circle", angle=45)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")
