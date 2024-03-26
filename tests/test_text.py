# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=duplicate-code

from drawlib._canvas import *
from drawlib._model import *
from drawlib._util import get_function_name
from drawlib.settings import set_suppress_warning

FONT_FILE = "./assets/font.ttf"
OUTPUT_DIR = "../tests_output/text/"


def test_text():
    clear()
    config(width=10, height=10, grid=True)
    text(3, 3, "Hello World")
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_text_font():
    set_suppress_warning(True)
    clear()
    config(width=10, height=10, grid=True)
    text(3, 3, "あいうえお")
    style = TextStyle(font_file=FONT_FILE)
    text(6, 6, "あいうえお", style=style)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_text_background():
    clear()
    config(width=10, height=10, grid=True)
    text(
        3,
        3,
        "Hello World",
        background=TextBackgroundStyle(
            boxstyle="larrow",
            lcolor="blue",
            fcolor="yellow",
            lstyle="dotted",
            lwidth=3,
        ),
        angle=90,
    )
    save(f"{OUTPUT_DIR}{get_function_name()}.png")
