# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Helper script for updating pyproject.toml

Check drawlib.__init__.py and get
- version
- lib name
- author
- contact

Then, updadate pyproject.toml
"""

import importlib.util
import os

TEMPLATE = """
# GENERATED CODE: START
# from drawlib.__init__.py

[tool.poetry]
name = "{lib_name}"
version = "{lib_version}"
description = "{description}"
homepage = "{homepage}"
repository = "{repository}"
authors = {authors}
readme = "{readme}"

# GENERATED CODE: END
""".strip()

TEMPLATE_START_SEQUENCE = "# GENERATED CODE: START"
TEMPLATE_END_SEQUENCE = "# GENERATED CODE: END"


def cd_to_project_root():
    """Change directory to project root."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    os.chdir("../")


def update_pyproject_toml():
    """Update pyproject.toml from drawlib.__init__.py"""
    spec = importlib.util.spec_from_file_location("init", "drawlib/__init__.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load module")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    lib_version = module.LIB_VERSION
    lib_name = module.LIB_NAME
    description = module.DESCRIPTION
    homepage = module.HOMEPAGE
    repository = module.REPOSITORY
    authors = module.AUTHORS
    readme = module.README

    # read
    with open("pyproject.toml", mode="r", encoding="utf8") as fin:
        read_text = fin.read()

    # create template
    authors_lines = ["["]
    for author in authors:
        authors_lines.append(f'    "{author}",')
    authors_lines.append("]")
    authors_text = "\n".join(authors_lines)

    generated_code = TEMPLATE.format(
        lib_name=lib_name,
        lib_version=lib_version,
        description=description,
        homepage=homepage,
        repository=repository,
        authors=authors_text,
        readme=readme,
    )

    # create write text
    is_template_line = False
    write_lines = []
    for line in read_text.splitlines():
        if line == TEMPLATE_START_SEQUENCE:
            is_template_line = True
            write_lines.append(generated_code)
            continue
        if line == TEMPLATE_END_SEQUENCE:
            is_template_line = False
            continue
        if is_template_line:
            continue
        write_lines.append(line)

    write_text = "\n".join(write_lines)

    # write
    with open("pyproject.toml", mode="w", encoding="utf8") as fout:
        fout.write(write_text)


if __name__ == "__main__":
    cd_to_project_root()
    update_pyproject_toml()
