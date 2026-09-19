from typing import Literal

from drawlib.apis import *

COLOR_TEMPLATE = "- ``{name}``: RGB{code}"

IMAGE_TEMPLATE = """
Style ``{name}``

.. figure:: image_style_{name}.png
    :width: 600
    :class: with-border
    :align: center

    Theme Style {name}
""".strip()


def print_color(theme: Literal["default", "essentials", "monochrome"]):
    dtheme.apply_official_theme(theme)
    for color in dtheme.colors.list():
        code = dtheme.colors.get(color)[:3]
        print(COLOR_TEMPLATE.format(name=color, code=str(code)))


def print_image(theme: Literal["default", "essentials", "monochrome"]):
    dtheme.apply_official_theme(theme)
    for color in dtheme.colors.list():
        print(IMAGE_TEMPLATE.format(name=color))
        print()


print_color("default")
