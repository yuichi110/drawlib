from drawlib import *
import drawlib


def test_all_doc_exist():
    module_objects = set()
    g = globals()
    for object_name in dir(drawlib):
        if object_name.startswith("_"):
            continue
        if "drawlib" in object_name:
            continue
        module_objects.add(g[object_name])

    all_drawlib_objects_have_doc = True
    for module_object in module_objects:
        if module_object.__doc__ is None:
            print(f"'{module_object.__name__}' has no doc.")
            all_drawlib_objects_have_doc = False

    assert all_drawlib_objects_have_doc


def test_all_webdoc_exist(): ...
