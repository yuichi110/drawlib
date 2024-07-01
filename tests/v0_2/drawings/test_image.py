# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from PIL import Image

from drawlib.v0_2.apis import *

IMAGE_FILE = "../../assets/image.png"
OUTPUT_DIR = "../../../output_tests/v0_2/drawings/image/"


def test_file():
    image(xy=(50, 50), width=30, image=IMAGE_FILE)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_pil():
    path = dutil_script.get_relative_path(IMAGE_FILE)
    im = Image.open(path)
    image(xy=(50, 50), width=30, image=im)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_pimage():
    pimg = Dimage(IMAGE_FILE)
    image(xy=(50, 50), width=30, image=pimg)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_cache():
    pimg = Dimage(IMAGE_FILE)
    Dimage.cache.set("linux", pimg)
    assert Dimage.cache.list() == ["linux"]
    pimg2 = Dimage.cache.get("linux")
    image(xy=(50, 50), width=30, image=pimg2)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_file_angle45():
    image(xy=(50, 50), width=30, angle=45, image=IMAGE_FILE)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_file_angle90():
    image(xy=(50, 50), width=30, angle=90, image=IMAGE_FILE)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_file_angle135():
    image(xy=(50, 50), width=30, angle=135, image=IMAGE_FILE)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_file_border():
    image(
        xy=(25, 50),
        width=30,
        image=IMAGE_FILE,
        style=ImageStyle(lwidth=2),
    )

    image(
        xy=(55, 25),
        width=30,
        image=IMAGE_FILE,
        style=ImageStyle(lwidth=2, halign="left", valign="bottom"),
    )

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_file_fill():
    image(
        xy=(50, 50),
        width=30,
        image=IMAGE_FILE,
        style=ImageStyle(fcolor=Colors.Gray),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_file_alpha():
    config(grid_only=True, background_color=Colors.Gray)
    image(
        xy=(50, 50),
        width=30,
        image=IMAGE_FILE,
        style=ImageStyle(alpha=0.1),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_file_border_angle45():
    image(
        xy=(50, 50),
        width=30,
        image=IMAGE_FILE,
        angle=45,
        style=ImageStyle(lwidth=2),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
