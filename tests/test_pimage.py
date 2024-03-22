from drawlib import *
from PIL import Image

IMAGE_FILE = "tests_input/image.png"
FONT_FILE = "tests_input/font.ttf"
OUTPUT_DIR = "tests_output/pimage/"


def test_file():
    img = Pimage(IMAGE_FILE)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_pil_image():
    pil_img = Image.open(IMAGE_FILE)
    img = Pimage(pil_img)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_rotate45():
    img = Pimage(IMAGE_FILE).rotate(45)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_rotate90():
    img = Pimage(IMAGE_FILE).rotate(90)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_rotate180():
    img = Pimage(IMAGE_FILE).rotate(180)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_resize():
    img = Pimage(IMAGE_FILE).resize(100, 200)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_flip():
    img = Pimage(IMAGE_FILE).flip()
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_mirror():
    img = Pimage(IMAGE_FILE).mirror()
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_invert():
    img = Pimage(IMAGE_FILE).invert()
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_grayscale():
    img = Pimage(IMAGE_FILE).grayscale()
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_brightness():
    img = Pimage(IMAGE_FILE).brightness(0.5)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_sepia():
    img = Pimage(IMAGE_FILE).sepia()
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_colorize():
    img = Pimage(IMAGE_FILE).colorize(black="blue", white="red")
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_posterize():
    img = Pimage(IMAGE_FILE).posterize()
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_mosaic():
    img = Pimage(IMAGE_FILE).mosaic()
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_blur():
    img = Pimage(IMAGE_FILE).blur()
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_line_extraction():
    img = Pimage(IMAGE_FILE).line_extraction()
    save(f"{OUTPUT_DIR}{get_function_name()}.png")
