# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import dataclasses

from drawlib.apis import (
    circle,
    config,
    dtheme,
    dutil_script,
    icon_phosphor,
    image,
    line,
    rectangle,
    save,
    text,
)
from drawlib.v0_2.private.l3_fonts import FontSansSerif, FontSourceCode
from drawlib.v0_2.private.l3_styles import (
    Colors,
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)
from drawlib.v0_2.private.l4_theme._theme_models import OfficialThemeStyle
from drawlib.v0_2.private.l4_theme._theme_officials import (
    OfficialThemeTemplate,
    get_default,
    get_essentials,
    get_monochrome,
)

IMAGE_FILE = "../../assets/image.png"
OUTPUT_DIR_ESSENTIALS = "../../../output_tests/v0_2/l4_theme/essentials/"
OUTPUT_DIR_MONOCHROME = "../../../output_tests/v0_2/l4_theme/monochrome/"


def test_official_theme_template() -> None:
    """Verifies that OfficialThemeTemplate is a dataclass and instantiates correctly."""
    template = OfficialThemeTemplate(
        icon_style="light",
        icon_color=(0, 0, 0, 1.0),
        image_line_width=0.0,
        line_style="solid",
        line_width=2.0,
        line_color=(0, 0, 0, 1.0),
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1.5,
        shape_line_color=(0, 0, 0, 1.0),
        shape_fill_color=(0, 0, 255, 1.0),
        shapetext_font=FontSansSerif.RALEWAYS_REGULAR,
        shapetext_size=16,
        shapetext_color=(0, 0, 0, 1.0),
        text_font=FontSansSerif.RALEWAYS_REGULAR,
        text_size=16,
        text_color=(0, 0, 0, 1.0),
    )
    assert dataclasses.is_dataclass(template)
    assert template.icon_style == "light"
    assert template.line_width == 2.0


def test_official_theme_generators() -> None:
    """Verifies that all three official theme generation functions return valid instances."""
    default_theme = get_default()
    assert isinstance(default_theme, OfficialThemeStyle)
    assert len(default_theme.theme_colors) > 0

    essentials_theme = get_essentials()
    assert isinstance(essentials_theme, OfficialThemeStyle)
    assert len(essentials_theme.theme_colors) > 0

    monochrome_theme = get_monochrome()
    assert isinstance(monochrome_theme, OfficialThemeStyle)
    assert len(monochrome_theme.theme_colors) > 0


# ==========================================
# Essentials Theme Drawing Integration Tests
# ==========================================


def test_essentials_colors() -> None:
    """Integrated drawing test for essentials theme colors list."""
    dtheme.apply_official_theme("essentials")

    x_start = 10
    x_pad = 20
    y_start = 10
    y_pad = 20
    for i, color in enumerate(dtheme.colors.list()):
        row = int(i / 5)
        col = i % 5
        if color in {"navy", "charcoal", "graphite", "black"}:
            ts = "white"
        else:
            ts = ""
        rectangle(
            (x_start + x_pad * col, y_start + y_pad * row),
            width=15,
            height=10,
            text=color,
            style=color,
            textstyle=ts,
        )

    save(f"{OUTPUT_DIR_ESSENTIALS}test_colors.png")


def test_essentials_difficult_to_see_colors() -> None:
    """Integrated drawing test for yellow, ivory, snow on essentials."""
    dtheme.apply_official_theme("essentials")
    config(width=100, height=50, grid_only=False, grid=False)
    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 10
    y2 = 25
    y3 = 40

    for x, name in [(x1, "yellow"), (x2, "ivory"), (x3, "snow")]:
        line((x - 10, y1), (x + 10, y1), style=f"{name}_bold")
        circle((x, y2), radius=10, style=name)
        text((x, y3), "Hello Drawlib!", style=f"{name}_bold")

    save(f"{OUTPUT_DIR_ESSENTIALS}test_difficult_to_see_colors.png")


def test_essentials_fill() -> None:
    """Integrated drawing test for essentials circle filling styles."""
    dtheme.apply_official_theme("essentials")
    circle((25, 25), 10, text="drawlib")
    circle((25, 50), 10, style="blue", text="drawlib")
    circle((25, 75), 10, style="green", text="drawlib")
    circle((75, 25), 10, style="red", text="drawlib")
    circle((75, 50), 10, style="black", text="drawlib", textstyle="white")
    circle((75, 75), 10, style="white", text="drawlib")
    save(f"{OUTPUT_DIR_ESSENTIALS}test_fill.png")


def test_essentials_style_images() -> None:
    """Integrated drawing test for essentials image border styling."""
    dtheme.apply_official_theme("essentials")
    image((25, 25), 20, style="blue", image=IMAGE_FILE)
    image((25, 50), 20, style="blue_flat", image=IMAGE_FILE)
    image((25, 75), 20, style="blue_solid", image=IMAGE_FILE)
    image((50, 50), 20, style="blue_dashed", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR_ESSENTIALS}test_style_images.png")


def test_essentials_fill_images() -> None:
    """Integrated drawing test for essentials image fill colors."""
    dtheme.apply_official_theme("essentials")
    image((25, 25), 20, image=IMAGE_FILE)
    image((25, 50), 20, style="blue", image=IMAGE_FILE)
    image((25, 75), 20, style="green", image=IMAGE_FILE)
    image((75, 25), 20, style="red", image=IMAGE_FILE)
    image((75, 50), 20, style="black", image=IMAGE_FILE)
    image((75, 75), 20, style="white", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR_ESSENTIALS}test_fill_images.png")


def test_essentials_flat_images() -> None:
    """Integrated drawing test for essentials flat styled images."""
    dtheme.apply_official_theme("essentials")
    config(background_color=Colors.Gray)
    image((25, 25), 20, style="flat", image=IMAGE_FILE)
    image((25, 50), 20, style="blue_flat", image=IMAGE_FILE)
    image((25, 75), 20, style="green_flat", image=IMAGE_FILE)
    image((75, 25), 20, style="red_flat", image=IMAGE_FILE)
    image((75, 50), 20, style="black_flat", image=IMAGE_FILE)
    image((75, 75), 20, style="white_flat", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR_ESSENTIALS}test_flat_images.png")


def test_essentials_solid_images() -> None:
    """Integrated drawing test for essentials solid styled images."""
    dtheme.apply_official_theme("essentials")
    image((25, 25), 20, style="solid", image=IMAGE_FILE)
    image((25, 50), 20, style="blue_solid", image=IMAGE_FILE)
    image((25, 75), 20, style="green_solid", image=IMAGE_FILE)
    image((75, 25), 20, style="red_solid", image=IMAGE_FILE)
    image((75, 50), 20, style="black_solid", image=IMAGE_FILE)
    image((75, 75), 20, style="white_solid", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR_ESSENTIALS}test_solid_images.png")


def test_essentials_dashed_images() -> None:
    """Integrated drawing test for essentials dashed styled images."""
    dtheme.apply_official_theme("essentials")
    image((25, 25), 20, style="dashed", image=IMAGE_FILE)
    image((25, 50), 20, style="blue_dashed", image=IMAGE_FILE)
    image((25, 75), 20, style="green_dashed", image=IMAGE_FILE)
    image((75, 25), 20, style="red_dashed", image=IMAGE_FILE)
    image((75, 50), 20, style="black_dashed", image=IMAGE_FILE)
    image((75, 75), 20, style="white_dashed", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR_ESSENTIALS}test_dashed_images.png")


def test_essentials_flat() -> None:
    """Integrated drawing test for essentials flat circles."""
    dtheme.apply_official_theme("essentials")
    circle((25, 25), 10, style="flat", text="drawlib")
    circle((25, 50), 10, style="blue_flat", text="drawlib")
    circle((25, 75), 10, style="green_flat", text="drawlib")
    circle((75, 25), 10, style="red_flat", text="drawlib")
    circle((75, 50), 10, style="black_flat", text="drawlib", textstyle="white")
    circle((75, 75), 10, style="white_flat", text="drawlib")
    save(f"{OUTPUT_DIR_ESSENTIALS}test_flat.png")


def test_essentials_solid() -> None:
    """Integrated drawing test for essentials solid circles."""
    dtheme.apply_official_theme("essentials")
    circle((25, 25), 10, style="solid", text="drawlib")
    circle((25, 50), 10, style="blue_solid", text="drawlib")
    circle((25, 75), 10, style="green_solid", text="drawlib")
    circle((75, 25), 10, style="red_solid", text="drawlib")
    circle((75, 50), 10, style="black_solid", text="drawlib", textstyle="white")
    circle((75, 75), 10, style="white_solid", text="drawlib")
    save(f"{OUTPUT_DIR_ESSENTIALS}test_solid.png")


def test_essentials_dashed() -> None:
    """Integrated drawing test for essentials dashed circles."""
    dtheme.apply_official_theme("essentials")
    circle((25, 25), 10, style="dashed", text="drawlib")
    circle((25, 50), 10, style="blue_dashed", text="drawlib")
    circle((25, 75), 10, style="green_dashed", text="drawlib")
    circle((75, 25), 10, style="red_dashed", text="drawlib")
    circle((75, 50), 10, style="black_dashed", text="drawlib", textstyle="white")
    circle((75, 75), 10, style="white_dashed", text="drawlib")
    save(f"{OUTPUT_DIR_ESSENTIALS}test_dashed.png")


def test_essentials_style_print() -> None:
    """Integrated verification of essentials style table output."""
    dtheme.apply_official_theme("essentials")
    assert dtheme._get_style_table().startswith("+----------------+---+-------+------+------+")


def test_essentials_theme_colors_print() -> None:
    """Integrated verification of essentials theme colors print string."""
    dtheme.apply_official_theme("essentials")
    assert "red        :" in dtheme._get_theme_colors()


# ==========================================
# Monochrome Theme Drawing Integration Tests
# ==========================================


def test_monochrome_icon_text_lightbold() -> None:
    """Integrated drawing test for monochrome icons and text."""
    dtheme.apply_official_theme("monochrome")
    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 20
    y2 = 50
    y3 = 80

    icon_phosphor.airplane((x1, y1), width=20, style="light")
    icon_phosphor.airplane((x2, y1), width=20)
    icon_phosphor.airplane((x3, y1), width=20, style="bold")

    text((x1, y2), "Hello Drawlib1", style="light")
    text((x2, y2), "Hello Drawlib1")
    text((x3, y2), "Hello Drawlib1", style="bold")

    icon_phosphor.airplane((x1, y3), width=20, style="flat")
    icon_phosphor.airplane((x2, y3), width=20, style="black_flat")
    icon_phosphor.airplane((x3, y3), width=20, style="gray_flat")

    save(f"{OUTPUT_DIR_MONOCHROME}test_icon_text_lightbold.png")


def test_monochrome_shape_lightbold() -> None:
    """Integrated drawing test for monochrome circles with text."""
    dtheme.apply_official_theme("monochrome")
    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 20
    y2 = 50
    y3 = 80
    radius = 10

    circle((x1, y1), radius, style="light", text="drawlib", textstyle="light")
    circle((x2, y1), radius, text="drawlib")
    circle((x3, y1), radius, style="bold", text="drawlib", textstyle="bold")

    circle((x1, y2), radius, style="solid_light", text="drawlib", textstyle="light")
    circle((x2, y2), radius, style="solid", text="drawlib")
    circle((x3, y2), radius, style="solid_bold", text="drawlib", textstyle="bold")

    circle((x1, y3), radius, style="dashed_light", text="drawlib", textstyle="light")
    circle((x2, y3), radius, style="dashed", text="drawlib")
    circle((x3, y3), radius, style="dashed_bold", text="drawlib", textstyle="bold")

    save(f"{OUTPUT_DIR_MONOCHROME}test_shape_lightbold.png")


def test_monochrome_line_lightbold() -> None:
    """Integrated drawing test for monochrome line styles."""
    dtheme.apply_official_theme("monochrome")
    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 20
    y2 = 50
    y3 = 80

    line((x1 - 5, y1), (x1 + 5, y1), style="light")
    line((x2 - 5, y1), (x2 + 5, y1))
    line((x3 - 5, y1), (x3 + 5, y1), style="bold")

    line((x1 - 5, y2), (x1 + 5, y2), style="solid_light")
    line((x2 - 5, y2), (x2 + 5, y2), style="solid")
    line((x3 - 5, y2), (x3 + 5, y2), style="solid_bold")

    line((x1 - 5, y3), (x2 - 5, y3), style="dashed_light")
    line((x2 - 5, y3), (x3 - 5, y3), style="dashed")
    line((x3 - 5, y3), (x3 + 5, y3), style="dashed_bold")

    save(f"{OUTPUT_DIR_MONOCHROME}test_line_lightbold.png")


def test_monochrome_image_lightbold() -> None:
    """Integrated drawing test for monochrome image styles."""
    dtheme.apply_official_theme("monochrome")
    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 20
    y2 = 50
    y3 = 80
    width = 10

    image((x1, y1), width=width, image=IMAGE_FILE, style="light")
    image((x2, y1), width=width, image=IMAGE_FILE)
    image((x3, y1), width=width, image=IMAGE_FILE, style="bold")

    image((x1, y2), width=width, image=IMAGE_FILE, style="solid_light")
    image((x2, y2), width=width, image=IMAGE_FILE, style="solid")
    image((x3, y2), width=width, image=IMAGE_FILE, style="solid_bold")

    image((x1, y3), width=width, image=IMAGE_FILE, style="dashed_light")
    image((x2, y3), width=width, image=IMAGE_FILE, style="dashed")
    image((x3, y3), width=width, image=IMAGE_FILE, style="dashed_bold")

    save(f"{OUTPUT_DIR_MONOCHROME}test_image_lightbold.png")


def test_monochrome_fill() -> None:
    """Integrated drawing test for monochrome fills."""
    dtheme.apply_official_theme("monochrome")
    styles = [""] + dtheme.colors.list()
    xs = [20, 50, 80]
    ys = [20, 50, 80]
    for i, style in enumerate(styles):
        x = xs[int(i % 3)]
        y = ys[int(i / 3)]
        circle((x, y), 10, text=style, style=style)

    save(f"{OUTPUT_DIR_MONOCHROME}test_fill.png")


def test_monochrome_style_print() -> None:
    """Integrated verification of monochrome style table output."""
    dtheme.apply_official_theme("monochrome")
    assert dtheme._get_style_table().startswith("+----------------+---+-------+------+------+")


def test_monochrome_theme_colors_print() -> None:
    """Integrated verification of monochrome theme colors print string."""
    dtheme.apply_official_theme("monochrome")
    assert "black   :" in dtheme._get_theme_colors()
