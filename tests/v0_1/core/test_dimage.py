# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from PIL import Image

from drawlib.v0_1.apis import *

IMAGE_FILE = "../../assets/image.png"
FONT_FILE = "../../assets/font.ttf"
OUTPUT_DIR = "../../../output_tests/v0_1/core/dimage/"


def test_file():
    img = Dimage(IMAGE_FILE)
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_pil_image():
    path = dutil_script.get_relative_path(IMAGE_FILE)
    pil_img = Image.open(path)
    img = Dimage(pil_img)
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


"""
def test_rotate45():
    img = Dimage(IMAGE_FILE).rotate(45)
    img.save(f"{OUTPUT_DIR}{dutil.get_function_name()}.png")


def test_rotate90():
    img = Dimage(IMAGE_FILE).rotate(90)
    img.save(f"{OUTPUT_DIR}{dutil.get_function_name()}.png")


def test_rotate180():
    img = Dimage(IMAGE_FILE).rotate(180)
    img.save(f"{OUTPUT_DIR}{dutil.get_function_name()}.png")
"""


def test_resize():
    img = Dimage(IMAGE_FILE).resize(100, 200)
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_fill1():
    img = Dimage(IMAGE_FILE).fill(Colors.Gray)
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_fill2():
    img = Dimage(IMAGE_FILE).alpha(0.3).fill(Colors.Gray)
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_alpha():
    img = Dimage(IMAGE_FILE).alpha(0.3)
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_crop():
    width, height = Dimage(IMAGE_FILE).get_image_size()
    img = Dimage(IMAGE_FILE).crop(int(width / 5), int(height / 5), int(width * 3 / 5), int(height * 3 / 5))
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_flip():
    img = Dimage(IMAGE_FILE).flip()
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_mirror():
    img = Dimage(IMAGE_FILE).mirror()
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_invert():
    img = Dimage(IMAGE_FILE).invert()
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_grayscale():
    img = Dimage(IMAGE_FILE).grayscale()
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_brightness():
    img = Dimage(IMAGE_FILE).brightness(0.5)
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_sepia():
    img = Dimage(IMAGE_FILE).sepia()
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_colorize():
    img = Dimage(IMAGE_FILE).colorize(from_black_to=Colors.Blue, from_white_to=(255, 0, 0, 1.0))
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_colorize_mid():
    img = Dimage(IMAGE_FILE).colorize(
        from_black_to=Colors.Blue,
        from_white_to=Colors.Red,
        from_mid_to=Colors.Green,
    )
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_posterize():
    img = Dimage(IMAGE_FILE).posterize()
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_mosaic_bs8():
    img = Dimage(IMAGE_FILE).mosaic(block_size=8)
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_mosaic_bs16():
    img = Dimage(IMAGE_FILE).mosaic(block_size=16)
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_blur():
    img = Dimage(IMAGE_FILE).blur()
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_line_extraction():
    img = Dimage(IMAGE_FILE).line_extraction()
    image((50, 50), 50, img)
    img.save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_dimage.png")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
