# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/fonts/arabic/"


def test_kufi():
    text(
        (50, 10),
        "Hello World. لمّا كان الاعتراف بالكرامة المتأصلة في جميع",
        style=TextStyle(font=FontArabic.KUFI_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. لمّا كان الاعتراف بالكرامة المتأصلة في جميع",
        style=TextStyle(font=FontArabic.KUFI_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. لمّا كان الاعتراف بالكرامة المتأصلة في جميع",
        style=TextStyle(font=FontArabic.KUFI_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_naskh():
    text(
        (50, 30),
        "Hello World. لمّا كان الاعتراف بالكرامة المتأصلة في جميع",
        style=TextStyle(font=FontArabic.NASKH_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. لمّا كان الاعتراف بالكرامة المتأصلة في جميع",
        style=TextStyle(font=FontArabic.NASKH_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_sans():
    text(
        (50, 10),
        "Hello World. لمّا كان الاعتراف بالكرامة المتأصلة في جميع",
        style=TextStyle(font=FontArabic.SANSSERIF_LIGHT),
    )
    text(
        (50, 30),
        "Hello World. لمّا كان الاعتراف بالكرامة المتأصلة في جميع",
        style=TextStyle(font=FontArabic.SANSSERIF_REGULAR),
    )
    text(
        (50, 50),
        "Hello World. لمّا كان الاعتراف بالكرامة المتأصلة في جميع",
        style=TextStyle(font=FontArabic.SANSSERIF_BOLD),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
