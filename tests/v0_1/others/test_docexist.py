# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import inspect

import drawlib.v0_1.apis


def test_all_doc_exist():
    members = inspect.getmembers(drawlib.v0_1.apis)
    drawlib_members = [o[1] for o in members if not o[0].startswith("__")]

    all_drawlib_objects_have_doc = True
    for drawlib_object in drawlib_members:
        if drawlib_object.__doc__ is None:
            print(f"'{drawlib_object.__name__}' has no doc.")
            all_drawlib_objects_have_doc = False

    assert all_drawlib_objects_have_doc
