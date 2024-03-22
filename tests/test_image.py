from drawlib import *
from PIL import Image
import inspect

IMAGE_FILE = "tests_input/image.png"
OUTPUT_DIR = "tests_output/image/"


def test_image_file():
    clear()
    config(width=10, height=10, grid=True)
    image(1, 1, IMAGE_FILE, zoom=0.1)
    save(f"{OUTPUT_DIR}{inspect.stack()[0][3]}.png")


def test_image_pil():
    clear()
    config(width=10, height=10, grid=True)
    im = Image.open(IMAGE_FILE)
    image(1, 1, pilimg=im, zoom=0.1)
    save(f"{OUTPUT_DIR}{inspect.stack()[0][3]}.png")
