# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_1.apis import *


def test_iconstyle():
    style1 = IconStyle(style="thin", color=Colors.Red)
    style2 = IconStyle(halign="left")
    style3 = style1.merge(style2)

    assert style1 == IconStyle(style="thin", color=Colors.Red)
    assert style2 == IconStyle(halign="left")
    assert style3 == IconStyle(style="thin", color=Colors.Red, halign="left")
