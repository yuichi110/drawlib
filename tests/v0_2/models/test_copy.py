# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *


def test_iconstyle():
    style1 = IconStyle(style="thin", color=Colors.Red)
    style2 = style1.copy()

    assert id(style1) != id(style2)
    assert style1 == style2


def test_imagestyle():
    style1 = ImageStyle(halign="left", lstyle="dashed", lwidth=1)
    style2 = style1.copy()

    assert id(style1) != id(style2)
    assert style1 == style2


def test_linestyle():
    style1 = LineStyle(color=Colors.Red)
    style2 = style1.copy()

    assert id(style1) != id(style2)
    assert style1 == style2


def test_shapestyle():
    style1 = ShapeStyle(lcolor=Colors.Red)
    style2 = style1.copy()

    assert id(style1) != id(style2)
    assert style1 == style2


def test_shapetextstyle():
    style1 = ShapeTextStyle(color=Colors.Red)
    style2 = style1.copy()

    assert id(style1) != id(style2)
    assert style1 == style2


def test_textstyle():
    style1 = TextStyle(color=Colors.Red)
    style2 = style1.copy()

    assert id(style1) != id(style2)
    assert style1 == style2
