# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/dsarts/sourcecode/"

code_snippet = """
import math

def example_function(x):
    return x * 2

print(example_function(5))

class Hello:
    ...
""".strip()

init_content = """
# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.
""".strip()


def test():
    sc = dsart.SourceCode(
        language="python",
        style="default",
    )
    sc.draw(xy=(20, 20), width=30, code=code_snippet)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_styles():
    for x, y, style in [
        (5, 5, "bw"),
        (5, 35, "sas"),
        (5, 60, "staroffice"),
        (40, 5, "xcode"),
        (40, 35, "default"),
        (40, 60, "monokai"),
        (70, 5, "lightbulb"),
        (70, 35, "github-dark"),
        (70, 60, "rrt"),
    ]:
        sc = dsart.SourceCode(
            language="python",
            style=style,
            font=FontSourceCode.ROBOTO_MONO,
        )
        sc.draw(xy=(x, y), width=25, code=code_snippet)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_styles2():
    for x, y, style in [
        (5, 5, "algol"),
        (5, 35, "algol_nu"),
        (5, 65, "friendly_grayscale"),
    ]:
        sc = dsart.SourceCode(
            language="python",
            style=style,
            font=FontSourceCode.ROBOTO_MONO,
        )
        sc.draw(xy=(x, y), width=25, code=code_snippet)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_font():
    for x, y, style in [
        (5, 5, "bw"),
        (5, 35, "sas"),
        (5, 60, "staroffice"),
        (40, 5, "xcode"),
        (40, 35, "default"),
        (40, 60, "monokai"),
        (70, 5, "lightbulb"),
        (70, 35, "github-dark"),
        (70, 60, "rrt"),
    ]:
        sc = dsart.SourceCode(
            language="python",
            style=style,
            font=FontSourceCode.COURIER,
        )
        sc.draw(xy=(x, y), width=25, code=code_snippet)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_get_text():
    text = dsart.SourceCode.get_text("__init__.py").strip()
    assert text == init_content
