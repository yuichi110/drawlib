# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Helper script for updating pyproject.toml

Check src/drawlib/__init__.py and get
- version
- lib name
- author
- contact

Then, update pyproject.toml using tomlkit to preserve formatting.
"""

import importlib.util
import os
import re
from typing import Any

import tomlkit
from utils import cd_to_project_root

INIT_PATH = "src/drawlib/__init__.py"
PYPROJECT_TOML_PATH = "pyproject.toml"


def update_pyproject_toml() -> None:
    """Update pyproject.toml from src/drawlib/__init__.py"""
    # Load metadata from src/drawlib/__init__.py
    spec = importlib.util.spec_from_file_location("init", INIT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {INIT_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    lib_version = module.LIB_VERSION
    lib_name = module.LIB_NAME
    description = module.DESCRIPTION
    homepage = module.HOMEPAGE
    repository = module.REPOSITORY
    authors = module.AUTHORS
    readme = module.README

    # Read pyproject.toml
    with open(PYPROJECT_TOML_PATH, mode="r", encoding="utf8") as fin:
        doc: Any = tomlkit.parse(fin.read())

    # Update [project] section
    if "project" not in doc:
        doc["project"] = tomlkit.table()

    project: Any = doc["project"]
    project["name"] = lib_name
    project["version"] = lib_version
    project["description"] = description
    project["readme"] = readme

    # Format authors: [{name = "...", email = "..."}]
    authors_list = tomlkit.array()
    for author_str in authors:
        match = re.match(r"(.*) <(.*)>", author_str)
        if match:
            name = match.group(1).strip()
            email = match.group(2).strip()
            author_dict = tomlkit.inline_table()
            author_dict.update({"name": name, "email": email})
            authors_list.append(author_dict)
        else:
            author_dict = tomlkit.inline_table()
            author_dict.update({"name": author_str.strip()})
            authors_list.append(author_dict)

    project["authors"] = authors_list

    # Update [project.urls] section
    if "urls" not in project:
        project["urls"] = tomlkit.table()

    urls: Any = project["urls"]
    urls["Homepage"] = homepage
    urls["Repository"] = repository

    # Write back
    with open(PYPROJECT_TOML_PATH, mode="w", encoding="utf8", newline="") as fout:
        fout.write(tomlkit.dumps(doc))


if __name__ == "__main__":
    cd_to_project_root()
    update_pyproject_toml()
    print("Successfully updated pyproject.toml metadata from src/drawlib/__init__.py")
