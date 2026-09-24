# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603

"""Integration tests for drawlib init CLI command and project scaffolding API."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from drawlib.tools import init_project, list_project_types


def run_drawlib_cli(args: list[str], cwd: str) -> subprocess.CompletedProcess[str]:
    """Helper to execute drawlib CLI command via subprocess with current PYTHONPATH.

    Args:
        args: Command line arguments.
        cwd: Working directory for execution.

    Returns:
        CompletedProcess: Subprocess result.
    """
    env = os.environ.copy()
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
    env["PYTHONPATH"] = src_dir + os.pathsep + env.get("PYTHONPATH", "")

    cmd = [sys.executable, "-m", "drawlib"] + args
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, check=False)


def test_cli_init_list(tmp_path: Path) -> None:
    """Test `drawlib init --list` and `-l` display available project types."""
    res1 = run_drawlib_cli(["init", "--list"], cwd=str(tmp_path))
    assert res1.returncode == 0
    assert "Available Drawlib Project Types:" in res1.stdout
    assert "simple" in res1.stdout
    assert "site" in res1.stdout
    assert "pdf" in res1.stdout

    res2 = run_drawlib_cli(["init", "-l"], cwd=str(tmp_path))
    assert res2.returncode == 0
    assert "simple" in res2.stdout


def test_cli_init_missing_type(tmp_path: Path) -> None:
    """Test `drawlib init` without arguments exits with code 1."""
    res = run_drawlib_cli(["init"], cwd=str(tmp_path))
    assert res.returncode == 1
    assert "Error: Missing project type." in res.stderr
    assert "simple" in res.stderr


def test_cli_init_unknown_type(tmp_path: Path) -> None:
    """Test `drawlib init unknown` exits with code 1."""
    res = run_drawlib_cli(["init", "unknown"], cwd=str(tmp_path))
    assert res.returncode == 1
    assert "Error: Unknown project type 'unknown'." in res.stderr


def test_cli_init_simple(tmp_path: Path) -> None:
    """Test scaffolding a simple project."""
    dest = tmp_path / "my_simple"
    res = run_drawlib_cli(["init", "simple", str(dest)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert f"Initialized 'simple' project in {dest}" in res.stdout

    assert (dest / "README_DOCS.md").is_file()
    assert (dest / "docs_config.py").is_file()
    assert (dest / "docs_src" / "doc.md").is_file()

    build_sh = dest / "docs_build.sh"
    assert build_sh.is_file()
    assert os.stat(build_sh).st_mode & 0o111 != 0


def test_cli_init_site(tmp_path: Path) -> None:
    """Test scaffolding a documentation site project."""
    dest = tmp_path / "my_site"
    res = run_drawlib_cli(["init", "site", str(dest)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert f"Initialized 'site' project in {dest}" in res.stdout

    assert (dest / "README_DOCS.md").is_file()
    assert (dest / "docs_config.py").is_file()
    assert (dest / "docs_build.sh").is_file()
    assert (dest / "docs_src" / "index.md").is_file()
    assert (dest / "docs_src" / "architecture.md").is_file()
    assert (dest / "docs_src" / "workflow.md").is_file()


def test_cli_init_pdf(tmp_path: Path) -> None:
    """Test scaffolding a PDF project."""
    dest = tmp_path / "my_pdf"
    res = run_drawlib_cli(["init", "pdf", str(dest)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert f"Initialized 'pdf' project in {dest}" in res.stdout

    assert (dest / "README_DOCS.md").is_file()
    assert (dest / "docs_config.py").is_file()
    assert (dest / "docs_build.sh").is_file()
    assert (dest / "docs_src" / "00_cover.md").is_file()
    assert (dest / "docs_src" / "01_overview.md").is_file()
    assert (dest / "docs_src" / "02_design.md").is_file()


def test_cli_init_non_empty_error_and_force(tmp_path: Path) -> None:
    """Test non-empty directory triggers error unless --force is specified."""
    dest = tmp_path / "existing_dir"
    dest.mkdir()
    (dest / "some_file.txt").write_text("existing content", encoding="utf-8")

    # Without force
    res_err = run_drawlib_cli(["init", "simple", str(dest)], cwd=str(tmp_path))
    assert res_err.returncode == 1
    assert "is not empty" in res_err.stderr

    # With force
    res_ok = run_drawlib_cli(["init", "simple", str(dest), "--force"], cwd=str(tmp_path))
    assert res_ok.returncode == 0
    assert (dest / "docs_src" / "doc.md").is_file()


def test_cli_init_here(tmp_path: Path) -> None:
    """Test `drawlib init <type> --here` inside an existing repository with existing README.md."""
    repo_dir = tmp_path / "my_repo"
    repo_dir.mkdir()
    existing_readme = repo_dir / "README.md"
    existing_readme.write_text("# Existing Project\nOriginal readme content.", encoding="utf-8")
    (repo_dir / "app.py").write_text("print('hello')", encoding="utf-8")

    res = run_drawlib_cli(["init", "site", "--here"], cwd=str(repo_dir))
    assert res.returncode == 0
    assert "Initialized 'site' project in ." in res.stdout

    # Existing project files are completely preserved
    assert existing_readme.read_text(encoding="utf-8") == "# Existing Project\nOriginal readme content."
    assert (repo_dir / "app.py").read_text(encoding="utf-8") == "print('hello')"

    # Drawlib documentation files are created with docs_ prefix
    assert (repo_dir / "README_DOCS.md").is_file()
    assert (repo_dir / "docs_build.sh").is_file()
    assert (repo_dir / "docs_config.py").is_file()
    assert (repo_dir / "docs_src" / "index.md").is_file()

    # Second run without force fails because docs_src already exists
    res_conflict = run_drawlib_cli(["init", "site", "--here"], cwd=str(repo_dir))
    assert res_conflict.returncode == 1
    assert "already exists" in res_conflict.stderr

    # Second run with force succeeds
    res_force = run_drawlib_cli(["init", "site", "--here", "--force"], cwd=str(repo_dir))
    assert res_force.returncode == 0


def test_cli_init_here_conflict_destination(tmp_path: Path) -> None:
    """Test specifying both [DESTINATION] and --here raises error."""
    res = run_drawlib_cli(["init", "simple", "some_dir", "--here"], cwd=str(tmp_path))
    assert res.returncode == 1
    assert "Cannot specify both [DESTINATION] and --here." in res.stderr


def test_python_api_init(tmp_path: Path) -> None:
    """Test Python programmatic API for project initialization."""
    types = list_project_types()
    assert set(types.keys()) == {"simple", "site", "pdf"}

    target = tmp_path / "api_test"
    created = init_project("simple", destination=target)
    assert len(created) >= 4
    assert (target / "docs_build.sh").is_file()

    with pytest.raises(ValueError, match="Unknown project type"):
        init_project("invalid_type", destination=tmp_path / "invalid")

    with pytest.raises(FileExistsError, match="is not empty"):
        init_project("simple", destination=target, force=False)
