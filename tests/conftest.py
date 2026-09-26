# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

import pytest

from drawlib._utils import dutil_canvas, dutil_settings
from drawlib.canvas import config
from tests.utils import check_image_match

# Paths
REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_TESTS_DIR = REPO_ROOT / "output_tests"
TESTS_DIR = REPO_ROOT / "tests"


def _get_output_files(target_dir: Optional[Path] = None) -> dict[Path, float]:
    """Retrieve all PNG files and their modification times in target directory."""
    files: dict[Path, float] = {}
    scan_dir = target_dir if target_dir is not None else OUTPUT_TESTS_DIR
    if scan_dir.exists():
        for p in scan_dir.rglob("*.png"):
            try:
                files[p] = p.stat().st_mtime
            except FileNotFoundError:
                pass
    return files


def _get_answers_file_path(gen_file_abs: Path, test_module_abs: Path) -> Optional[Path]:
    """Map a generated file path to the corresponding expected answer file path.

    Returns None if the generated file does not belong to this test module or has no answer file.
    """
    try:
        subpath = test_module_abs.parent.relative_to(TESTS_DIR)
        rel_gen = gen_file_abs.relative_to(OUTPUT_TESTS_DIR)
    except ValueError:
        return None

    subpath_str = str(subpath).replace("\\", "/")
    rel_gen_str = str(rel_gen).replace("\\", "/")

    prefix = f"{subpath_str}/" if subpath_str != "." else ""
    if prefix and not rel_gen_str.startswith(prefix):
        return None

    suffix = rel_gen_str[len(prefix) :] if prefix else rel_gen_str

    module_name_clean = test_module_abs.stem.replace("test_", "")
    suffix_parts = suffix.split("/")
    if suffix_parts[0] == module_name_clean:
        suffix = "/".join(suffix_parts[1:])

    answers_dir = test_module_abs.parent / f"{test_module_abs.stem}_answers"
    answer_file = answers_dir / suffix
    if not answer_file.is_file():
        return None
    return answer_file


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
    test_module_path = Path(item.module.__file__)
    try:
        subpath = test_module_path.parent.relative_to(TESTS_DIR)
        module_output_dir = OUTPUT_TESTS_DIR / subpath
    except ValueError:
        module_output_dir = OUTPUT_TESTS_DIR

    # Track output images before the test in this module's target directory
    files_before = _get_output_files(module_output_dir)

    # Execute the test function
    outcome = yield

    # If the test function itself raised an exception, do not assert image matches
    try:
        outcome.get_result()
    except Exception:
        return

    # Track output images after the test in this module's target directory
    files_after = _get_output_files(module_output_dir)

    # Identify files that were created or modified during the test
    modified_files = []
    for p, mtime in files_after.items():
        if p not in files_before or mtime > files_before[p]:
            modified_files.append(p)

    for gen_file in modified_files:
        correct_file = _get_answers_file_path(gen_file, test_module_path)
        if correct_file is None:
            continue

        with open(gen_file, "rb") as f:
            gen_bytes = f.read()

        marker = item.get_closest_marker("image_threshold")
        threshold = float(marker.args[0]) if marker and marker.args else 99.0
        # Verify that the generated image matches the reference answer image
        assert check_image_match(gen_bytes, correct_file=correct_file, threshold=threshold), (
            f"Image match failed for: {gen_file} against expected {correct_file}"
        )
