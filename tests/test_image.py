from PIL import Image
from drawlib._canvas import *
from drawlib._util import get_script_relative_path, get_function_name


IMAGE_FILE = "./assets/image.png"
OUTPUT_DIR = "../tests_output/image/"


def test_image_file():
    clear()
    config(width=10, height=10, grid=True)
    image(1, 1, IMAGE_FILE, zoom=0.1)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")


def test_image_pil():
    clear()
    config(width=10, height=10, grid=True)
    path = get_script_relative_path(IMAGE_FILE)
    im = Image.open(path)
    image(1, 1, pilimg=im, zoom=0.1)
    save(f"{OUTPUT_DIR}{get_function_name()}.png")
