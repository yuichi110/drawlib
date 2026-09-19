TEMPLATE = """
style ``{color}``

.. figure:: image_style_{color}.png
    :width: 600
    :class: with-border
    :align: center

    style {color}
""".strip()


def print_colors(colors: list[str]):
    for color in colors:
        print(f"- ``{color}``")


def print_styles(colors: list[str]):
    for color in colors:
        text = TEMPLATE.format(color=color)
        print(text)
        print()


colors = [
    "turquoise",
    "green_sea",
    "emerald",
    "nephritis",
    "peter_river",
    "belize_hole",
    "amethyst",
    "wisteria",
    "wet_asphalt",
    "midnight_blue",
    "sun_flower",
    "orange",
    "carrot",
    "pumpkin",
    "alizarin",
    "pomegranate",
    "clouds",
    "silver",
    "concrete",
    "asbestos",
    "black",
    "white",
]

print_colors(colors)
print_styles(colors)
