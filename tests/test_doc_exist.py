# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=duplicate-code

import inspect
import drawlib.advance


def test_all_doc_exist():
    members = inspect.getmembers(drawlib.advance)
    drawlib_members = [o[1] for o in members if not o[0].startswith("__")]

    all_drawlib_objects_have_doc = True
    for drawlib_object in drawlib_members:
        if drawlib_object.__doc__ is None:
            print(f"'{drawlib_object.__name__}' has no doc.")
            all_drawlib_objects_have_doc = False

    assert all_drawlib_objects_have_doc


def test_all_webdoc_exist(): ...
