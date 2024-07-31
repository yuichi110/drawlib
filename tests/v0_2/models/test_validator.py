# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa
# type: ignore

from dataclasses import asdict

import pytest

from drawlib.v0_2.apis import *


def test_icon_style():
    assert asdict(IconStyle()) == {
        "style": None,
        "color": None,
        "alpha": None,
        "halign": None,
        "valign": None,
    }
    assert asdict(IconStyle(style="thin")) == {
        "style": "thin",
        "color": None,
        "alpha": None,
        "halign": None,
        "valign": None,
    }
    assert asdict(IconStyle(color=Colors.Red)) == {
        "style": None,
        "color": Colors.Red,
        "alpha": None,
        "halign": None,
        "valign": None,
    }
    assert asdict(IconStyle(color=(100, 100, 100))) == {
        "style": None,
        "color": (100, 100, 100),
        "alpha": None,
        "halign": None,
        "valign": None,
    }
    assert asdict(IconStyle(color=(100, 100, 100, 0.5))) == {
        "style": None,
        "color": (100, 100, 100, 0.5),
        "alpha": None,
        "halign": None,
        "valign": None,
    }
    assert asdict(IconStyle(alpha=0.5)) == {
        "style": None,
        "color": None,
        "alpha": 0.5,
        "halign": None,
        "valign": None,
    }
    assert asdict(IconStyle(halign="left")) == {
        "style": None,
        "color": None,
        "alpha": None,
        "halign": "left",
        "valign": None,
    }
    assert asdict(IconStyle(valign="bottom")) == {
        "style": None,
        "color": None,
        "alpha": None,
        "halign": None,
        "valign": "bottom",
    }

    with pytest.raises(ValueError):
        IconStyle(style="wrong")
    with pytest.raises(ValueError):
        IconStyle(color=0.1)
    with pytest.raises(ValueError):
        IconStyle(color=(100, 100, 1000))
    with pytest.raises(ValueError):
        IconStyle(color=(100, 100, 100, 10))
    with pytest.raises(ValueError):
        IconStyle(halign="wrong")
    with pytest.raises(ValueError):
        IconStyle(valign="wrong")


def test_image_style():
    assert asdict(ImageStyle()) == {
        "halign": None,
        "valign": None,
        "lwidth": None,
        "lstyle": None,
        "lcolor": None,
        "fcolor": None,
        "alpha": None,
    }
    assert asdict(ImageStyle(halign="left")) == {
        "halign": "left",
        "valign": None,
        "lwidth": None,
        "lstyle": None,
        "lcolor": None,
        "fcolor": None,
        "alpha": None,
    }
    assert asdict(ImageStyle(valign="bottom")) == {
        "halign": None,
        "valign": "bottom",
        "lwidth": None,
        "lstyle": None,
        "lcolor": None,
        "fcolor": None,
        "alpha": None,
    }
    assert asdict(ImageStyle(lwidth=2)) == {
        "halign": None,
        "valign": None,
        "lwidth": 2,
        "lstyle": None,
        "lcolor": None,
        "fcolor": None,
        "alpha": None,
    }
    assert asdict(ImageStyle(lstyle="dashed")) == {
        "halign": None,
        "valign": None,
        "lwidth": None,
        "lstyle": "dashed",
        "lcolor": None,
        "fcolor": None,
        "alpha": None,
    }
    assert asdict(ImageStyle(lcolor=Colors.Red)) == {
        "halign": None,
        "valign": None,
        "lwidth": None,
        "lstyle": None,
        "lcolor": Colors.Red,
        "fcolor": None,
        "alpha": None,
    }
    assert asdict(ImageStyle(fcolor=Colors.Red)) == {
        "halign": None,
        "valign": None,
        "lwidth": None,
        "lstyle": None,
        "lcolor": None,
        "fcolor": Colors.Red,
        "alpha": None,
    }
    assert asdict(ImageStyle(alpha=0.3)) == {
        "halign": None,
        "valign": None,
        "lwidth": None,
        "lstyle": None,
        "lcolor": None,
        "fcolor": None,
        "alpha": 0.3,
    }
    with pytest.raises(ValueError):
        ImageStyle(halign="wrong")
    with pytest.raises(ValueError):
        ImageStyle(valign="wrong")
    with pytest.raises(ValueError):
        ImageStyle(lstyle="wrong")


def test_line_style():
    assert asdict(LineStyle()) == {
        "width": None,
        "style": None,
        "color": None,
        "alpha": None,
        "ahscale": None,
        "ahfill": None,
    }
    assert asdict(LineStyle(width=2)) == {
        "width": 2,
        "style": None,
        "color": None,
        "alpha": None,
        "ahscale": None,
        "ahfill": None,
    }
    assert asdict(LineStyle(style="dashed")) == {
        "width": None,
        "style": "dashed",
        "color": None,
        "alpha": None,
        "ahscale": None,
        "ahfill": None,
    }
    assert asdict(LineStyle(color=Colors.Red)) == {
        "width": None,
        "style": None,
        "color": Colors.Red,
        "alpha": None,
        "ahscale": None,
        "ahfill": None,
    }
    assert asdict(LineStyle(alpha=0.5)) == {
        "width": None,
        "style": None,
        "color": None,
        "alpha": 0.5,
        "ahscale": None,
        "ahfill": None,
    }

    with pytest.raises(ValueError):
        LineStyle(width="wrong")
    with pytest.raises(ValueError):
        LineStyle(style="wrong")
    with pytest.raises(ValueError):
        LineStyle(color="wrong")
    with pytest.raises(ValueError):
        LineStyle(alpha="wrong")


def test_shape_style():
    assert asdict(ShapeStyle()) == {
        "halign": None,
        "valign": None,
        "alpha": None,
        "lwidth": None,
        "lcolor": None,
        "lstyle": None,
        "fcolor": None,
    }
    assert asdict(ShapeStyle(halign="left")) == {
        "halign": "left",
        "valign": None,
        "alpha": None,
        "lwidth": None,
        "lcolor": None,
        "lstyle": None,
        "fcolor": None,
    }
    assert asdict(ShapeStyle(valign="bottom")) == {
        "halign": None,
        "valign": "bottom",
        "alpha": None,
        "lwidth": None,
        "lcolor": None,
        "lstyle": None,
        "fcolor": None,
    }

    assert asdict(ShapeStyle(alpha=0.5)) == {
        "halign": None,
        "valign": None,
        "alpha": 0.5,
        "lwidth": None,
        "lcolor": None,
        "lstyle": None,
        "fcolor": None,
    }
    assert asdict(ShapeStyle(lwidth=2)) == {
        "halign": None,
        "valign": None,
        "alpha": None,
        "lwidth": 2,
        "lcolor": None,
        "lstyle": None,
        "fcolor": None,
    }
    assert asdict(ShapeStyle(lcolor=Colors.Red)) == {
        "halign": None,
        "valign": None,
        "alpha": None,
        "lwidth": None,
        "lcolor": Colors.Red,
        "lstyle": None,
        "fcolor": None,
    }
    assert asdict(ShapeStyle(lstyle="dashed")) == {
        "halign": None,
        "valign": None,
        "alpha": None,
        "lwidth": None,
        "lcolor": None,
        "lstyle": "dashed",
        "fcolor": None,
    }
    assert asdict(ShapeStyle(fcolor=Colors.Red)) == {
        "halign": None,
        "valign": None,
        "alpha": None,
        "lwidth": None,
        "lcolor": None,
        "lstyle": None,
        "fcolor": Colors.Red,
    }

    with pytest.raises(ValueError):
        ShapeStyle(halign="wrong")
    with pytest.raises(ValueError):
        ShapeStyle(valign="wrong")
    with pytest.raises(ValueError):
        ShapeStyle(alpha="wrong")
    with pytest.raises(ValueError):
        ShapeStyle(lwidth="wrong")
    with pytest.raises(ValueError):
        ShapeStyle(lcolor="wrong")
    with pytest.raises(ValueError):
        ShapeStyle(lstyle="wrong")
    with pytest.raises(ValueError):
        ShapeStyle(fcolor="wrong")


def test_shapetext_style():
    assert asdict(ShapeTextStyle()) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": None,
        "valign": None,
        "font": None,
        "angle": None,
        "flip": None,
        "xy_shift": None,
        "xy_abs_shift": None,
    }
    assert asdict(ShapeTextStyle(alpha=0.5)) == {
        "alpha": 0.5,
        "color": None,
        "size": None,
        "halign": None,
        "valign": None,
        "font": None,
        "angle": None,
        "flip": None,
        "xy_shift": None,
        "xy_abs_shift": None,
    }
    assert asdict(ShapeTextStyle(color=Colors.Red)) == {
        "alpha": None,
        "color": Colors.Red,
        "size": None,
        "halign": None,
        "valign": None,
        "font": None,
        "angle": None,
        "flip": None,
        "xy_shift": None,
        "xy_abs_shift": None,
    }
    assert asdict(ShapeTextStyle(size=20)) == {
        "alpha": None,
        "color": None,
        "size": 20,
        "halign": None,
        "valign": None,
        "font": None,
        "angle": None,
        "flip": None,
        "xy_shift": None,
        "xy_abs_shift": None,
    }
    assert asdict(ShapeTextStyle(halign="left")) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": "left",
        "valign": None,
        "font": None,
        "angle": None,
        "flip": None,
        "xy_shift": None,
        "xy_abs_shift": None,
    }
    assert asdict(ShapeTextStyle(valign="bottom")) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": None,
        "valign": "bottom",
        "font": None,
        "angle": None,
        "flip": None,
        "xy_shift": None,
        "xy_abs_shift": None,
    }
    assert asdict(ShapeTextStyle(font=Font.SANSSERIF_BOLD)) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": None,
        "valign": None,
        "font": Font.SANSSERIF_BOLD,
        "angle": None,
        "flip": None,
        "xy_shift": None,
        "xy_abs_shift": None,
    }
    assert asdict(ShapeTextStyle(angle=90)) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": None,
        "valign": None,
        "font": None,
        "angle": 90,
        "flip": None,
        "xy_shift": None,
        "xy_abs_shift": None,
    }
    assert asdict(ShapeTextStyle(flip=True)) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": None,
        "valign": None,
        "font": None,
        "angle": None,
        "flip": True,
        "xy_shift": None,
        "xy_abs_shift": None,
    }
    assert asdict(ShapeTextStyle(xy_shift=(10, 10))) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": None,
        "valign": None,
        "font": None,
        "angle": None,
        "flip": None,
        "xy_shift": (10, 10),
        "xy_abs_shift": None,
    }
    assert asdict(ShapeTextStyle(xy_abs_shift=(10, 10))) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": None,
        "valign": None,
        "font": None,
        "angle": None,
        "flip": None,
        "xy_shift": None,
        "xy_abs_shift": (10, 10),
    }

    with pytest.raises(ValueError):
        ShapeTextStyle(alpha="wrong")
    with pytest.raises(ValueError):
        ShapeTextStyle(color="wrong")
    with pytest.raises(ValueError):
        ShapeTextStyle(size="wrong")
    with pytest.raises(ValueError):
        ShapeTextStyle(halign="wrong")
    with pytest.raises(ValueError):
        ShapeTextStyle(valign="wrong")
    with pytest.raises(ValueError):
        ShapeTextStyle(font="wrong")
    with pytest.raises(ValueError):
        ShapeTextStyle(angle="wrong")
    with pytest.raises(ValueError):
        ShapeTextStyle(flip="wrong")
    with pytest.raises(ValueError):
        ShapeTextStyle(xy_shift="wrong")


def test_text_style():
    assert asdict(TextStyle()) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": None,
        "valign": None,
        "font": None,
        "bgalpha": None,
        "bglcolor": None,
        "bglstyle": None,
        "bglwidth": None,
        "bgfcolor": None,
    }
    assert asdict(TextStyle(alpha=0.5)) == {
        "alpha": 0.5,
        "color": None,
        "size": None,
        "halign": None,
        "valign": None,
        "font": None,
        "bgalpha": None,
        "bglcolor": None,
        "bglstyle": None,
        "bglwidth": None,
        "bgfcolor": None,
    }
    assert asdict(TextStyle(color=Colors.Red)) == {
        "alpha": None,
        "color": Colors.Red,
        "size": None,
        "halign": None,
        "valign": None,
        "font": None,
        "bgalpha": None,
        "bglcolor": None,
        "bglstyle": None,
        "bglwidth": None,
        "bgfcolor": None,
    }
    assert asdict(TextStyle(size=20)) == {
        "alpha": None,
        "color": None,
        "size": 20,
        "halign": None,
        "valign": None,
        "font": None,
        "bgalpha": None,
        "bglcolor": None,
        "bglstyle": None,
        "bglwidth": None,
        "bgfcolor": None,
    }
    assert asdict(TextStyle(halign="left")) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": "left",
        "valign": None,
        "font": None,
        "bgalpha": None,
        "bglcolor": None,
        "bglstyle": None,
        "bglwidth": None,
        "bgfcolor": None,
    }
    assert asdict(TextStyle(valign="bottom")) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": None,
        "valign": "bottom",
        "font": None,
        "bgalpha": None,
        "bglcolor": None,
        "bglstyle": None,
        "bglwidth": None,
        "bgfcolor": None,
    }
    assert asdict(TextStyle(font=Font.SANSSERIF_BOLD)) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": None,
        "valign": None,
        "font": Font.SANSSERIF_BOLD,
        "bgalpha": None,
        "bglcolor": None,
        "bglstyle": None,
        "bglwidth": None,
        "bgfcolor": None,
    }

    assert asdict(TextStyle(bgalpha=0.5)) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": None,
        "valign": None,
        "font": None,
        "bgalpha": 0.5,
        "bglcolor": None,
        "bglstyle": None,
        "bglwidth": None,
        "bgfcolor": None,
    }
    assert asdict(TextStyle(bglcolor=Colors.Red)) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": None,
        "valign": None,
        "font": None,
        "bgalpha": None,
        "bglcolor": Colors.Red,
        "bglstyle": None,
        "bglwidth": None,
        "bgfcolor": None,
    }
    assert asdict(TextStyle(bglstyle="dashed")) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": None,
        "valign": None,
        "font": None,
        "bgalpha": None,
        "bglcolor": None,
        "bglstyle": "dashed",
        "bglwidth": None,
        "bgfcolor": None,
    }
    assert asdict(TextStyle(bglwidth=2)) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": None,
        "valign": None,
        "font": None,
        "bgalpha": None,
        "bglcolor": None,
        "bglstyle": None,
        "bglwidth": 2,
        "bgfcolor": None,
    }
    assert asdict(TextStyle(bgfcolor=Colors.Red)) == {
        "alpha": None,
        "color": None,
        "size": None,
        "halign": None,
        "valign": None,
        "font": None,
        "bgalpha": None,
        "bglcolor": None,
        "bglstyle": None,
        "bglwidth": None,
        "bgfcolor": Colors.Red,
    }

    with pytest.raises(ValueError):
        TextStyle(alpha="wrong")
    with pytest.raises(ValueError):
        TextStyle(color="wrong")
    with pytest.raises(ValueError):
        TextStyle(size="wrong")
    with pytest.raises(ValueError):
        TextStyle(halign="wrong")
    with pytest.raises(ValueError):
        TextStyle(valign="wrong")
    with pytest.raises(ValueError):
        TextStyle(font="wrong")
    with pytest.raises(ValueError):
        TextStyle(bgalpha="wrong")
    with pytest.raises(ValueError):
        TextStyle(bglcolor="wrong")
    with pytest.raises(ValueError):
        TextStyle(bglstyle="wrong")
    with pytest.raises(ValueError):
        TextStyle(bglwidth="wrong")
    with pytest.raises(ValueError):
        TextStyle(bgfcolor="wrong")
