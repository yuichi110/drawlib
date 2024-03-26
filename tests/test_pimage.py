from PIL import Image
from drawlib._pil import Pimage
from drawlib._util import get_script_relative_path
from drawlib._util import get_function_name


IMAGE_FILE = "./assets/image.png"
FONT_FILE = "./assets/font.ttf"
OUTPUT_DIR = "../tests_output/pimage/"


def test_file():
    img = Pimage(IMAGE_FILE)
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_pil_image():
    path = get_script_relative_path(IMAGE_FILE)
    pil_img = Image.open(path)
    img = Pimage(pil_img)
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_rotate45():
    img = Pimage(IMAGE_FILE).rotate(45)
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_rotate90():
    img = Pimage(IMAGE_FILE).rotate(90)
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_rotate180():
    img = Pimage(IMAGE_FILE).rotate(180)
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_resize():
    img = Pimage(IMAGE_FILE).resize(100, 200)
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_flip():
    img = Pimage(IMAGE_FILE).flip()
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_mirror():
    img = Pimage(IMAGE_FILE).mirror()
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_invert():
    img = Pimage(IMAGE_FILE).invert()
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_grayscale():
    img = Pimage(IMAGE_FILE).grayscale()
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_brightness():
    img = Pimage(IMAGE_FILE).brightness(0.5)
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_sepia():
    img = Pimage(IMAGE_FILE).sepia()
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_colorize():
    img = Pimage(IMAGE_FILE).colorize(black="blue", white="red")
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_posterize():
    img = Pimage(IMAGE_FILE).posterize()
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_mosaic():
    img = Pimage(IMAGE_FILE).mosaic()
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_blur():
    img = Pimage(IMAGE_FILE).blur()
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_line_extraction():
    img = Pimage(IMAGE_FILE).line_extraction()
    img.save(f"{OUTPUT_DIR}{get_function_name()}.png")
