# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import os
import sys
from pathlib import Path

import pytest

from drawlib.apis import *
from tests.v0_2.utils import check_image_match

# Paths
REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_TESTS_DIR = REPO_ROOT / "output_tests" / "v0_2"
TESTS_DIR = REPO_ROOT / "tests" / "v0_2"


def _get_output_files() -> dict[Path, float]:
    """Retrieve all PNG files and their modification times in output_tests/v0_2."""
    files = {}
    if OUTPUT_TESTS_DIR.exists():
        for p in OUTPUT_TESTS_DIR.rglob("*.png"):
            try:
                files[p] = p.stat().st_mtime
            except FileNotFoundError:
                pass
    return files


def _get_answers_file_path(gen_file_abs: Path, test_module_abs: Path) -> Path:
    """Map a generated file path to the corresponding expected answer file path."""
    subpath = test_module_abs.parent.relative_to(TESTS_DIR)
    subpath_str = str(subpath).replace("\\", "/")

    rel_gen = gen_file_abs.relative_to(OUTPUT_TESTS_DIR)
    rel_gen_str = str(rel_gen).replace("\\", "/")

    prefix = f"{subpath_str}/"
    if rel_gen_str.startswith(prefix):
        suffix = rel_gen_str[len(prefix):]
    else:
        suffix = gen_file_abs.name

    module_name_clean = test_module_abs.stem.replace("test_", "")
    suffix_parts = suffix.split("/")
    if suffix_parts[0] == module_name_clean:
        suffix = "/".join(suffix_parts[1:])

    answers_dir = test_module_abs.parent / f"{test_module_abs.stem}_answers"
    return answers_dir / suffix


@pytest.fixture(scope="function", autouse=True)
def preprocess():
    """Preprocess test setup and initialize drawlib canvas."""
    dutil_settings._set_suppress_warning(True)
    config(grid_only=True)
    yield
    dutil_canvas.initialize()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    """Intercept the test function execution to verify generated images in the call phase (FAILED status)."""
    # Track output images before the test
    files_before = _get_output_files()

    # Execute the test function
    outcome = yield

    # If the test function itself raised an exception, do not assert image matches
    try:
        outcome.get_result()
    except Exception:
        return

    # Track output images after the test
    files_after = _get_output_files()
    test_module_path = Path(item.module.__file__)

    # Identify files that were created or modified during the test
    modified_files = []
    for p, mtime in files_after.items():
        if p not in files_before or mtime > files_before[p]:
            modified_files.append(p)

    for gen_file in modified_files:
        correct_file = _get_answers_file_path(gen_file, test_module_path)
        with open(gen_file, "rb") as f:
            gen_bytes = f.read()

        # Verify that the generated image matches the reference answer image
        assert check_image_match(gen_bytes, correct_file=correct_file), (
            f"Image match failed for: {gen_file} against expected {correct_file}"
        )
