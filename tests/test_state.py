from drawlib import *
from drawlib.debug import get_function_name


FONT_FILE = "./assets/font.ttf"
OUTPUT_DIR = "../tests_output/state/"


def test_save_without_filename():
    clear()
    config(width=10, height=10, grid=True)
    circle(5, 5, 3)
    # file name should be "<module-name-who-call-save>.png"
    # save to module file directory
    save()


def test_title():
    clear()
    config(width=10, height=10, grid=True)
    title("Test Title", y=-0.1)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_title_font():
    clear()
    config(width=10, height=10, grid=True)
    style = TextStyle(font_file=FONT_FILE)
    title("タイトルのテスト", y=-0.1, style=style)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")
