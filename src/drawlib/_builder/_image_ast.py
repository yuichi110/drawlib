# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AST static analysis and target path resolution helpers for drawlib image builder."""

from __future__ import annotations

import ast
import os
from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any, Literal

from drawlib._builder._common import format_duplicate_output_error
from drawlib._core.l1_core import logger

if TYPE_CHECKING:
    from drawlib._builder.image_builder import DrawlibExecuter


def _is_save_call_node(node: ast.Call) -> bool:
    """Return True if an AST Call node invokes `save(...)` or `*.save(...)`."""
    return (isinstance(node.func, ast.Name) and node.func.id == "save") or (
        isinstance(node.func, ast.Attribute) and node.func.attr == "save"
    )


def _parse_static_save_call(node: ast.Call) -> tuple[str | None, str | None] | None:
    """Extract static `(call_file, call_format)` from an AST `save(...)` call node, or None if not static."""
    if not _is_save_call_call(node):
        return None

    call_file: str | None = None
    call_format: str | None = None

    for idx, arg in enumerate(node.args[:2]):
        if not isinstance(arg, ast.Constant) or not (isinstance(arg.value, str) or arg.value is None):
            return None
        if idx == 0:
            call_file = arg.value
        else:
            call_format = arg.value

    for kw in node.keywords:
        if kw.arg not in {"file", "format"}:
            continue
        if not isinstance(kw.value, ast.Constant) or not (isinstance(kw.value.value, str) or kw.value.value is None):
            return None
        if kw.arg == "file":
            call_file = kw.value.value
        else:
            call_format = kw.value.value

    return call_file, call_format


def _is_save_call_call(node: ast.Call) -> bool:
    """Internal alias checking if AST Call is a save invocation."""
    return _is_save_call_node(node)


class _SaveCallVisitor(ast.NodeVisitor):
    """AST visitor that counts `save()` calls and extracts static save arguments."""

    def __init__(self) -> None:
        self.save_count: int = 0
        self.static_saves: list[tuple[str | None, str | None, int]] = []

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802
        """Visit a Call node to detect `save(...)` invocations."""
        if _is_save_call_node(node):
            self.save_count += 1
            parsed = _parse_static_save_call(node)
            if parsed is not None:
                call_file, call_format = parsed
                self.static_saves.append((call_file, call_format, node.lineno))
        self.generic_visit(node)


def _has_local_imports(tree: ast.AST, script_dir: str, topdir_path: str) -> bool:
    """Check whether the AST imports any local Python modules from script_dir or topdir_path."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                top_mod = alias.name.split(".")[0]
                if os.path.exists(os.path.join(script_dir, f"{top_mod}.py")) or (
                    topdir_path and os.path.exists(os.path.join(topdir_path, top_mod))
                ):
                    return True
        elif isinstance(node, ast.ImportFrom):
            if node.level > 0:
                return True
            if node.module:
                top_mod = node.module.split(".")[0]
                if os.path.exists(os.path.join(script_dir, f"{top_mod}.py")) or (
                    topdir_path and os.path.exists(os.path.join(topdir_path, top_mod))
                ):
                    return True
    return False


def _extract_single_static_save(
    tree: ast.AST,
    script_dir: str,
    topdir_path: str = "",
) -> tuple[str | None, str | None] | None:
    """Extract static save arguments if script has no local module imports, else None."""
    if _has_local_imports(tree, script_dir, topdir_path):
        return None
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            res = _parse_static_save_call(node)
            if res is not None:
                return res
    return None


def resolve_effective_output_dir(
    output_dir: str | None,
    script_path: str,
    current_target_root: str = "",
    target_roots: Sequence[str] = (),
) -> str | None:
    """Compute the effective output directory for a script, preserving subdirectories if under a target dir."""
    if not output_dir:
        return None
    abs_output_dir = os.path.abspath(output_dir)
    abs_script_dir = os.path.dirname(os.path.abspath(script_path))

    candidate_roots: list[str] = []
    if current_target_root:
        candidate_roots.append(current_target_root)
    if target_roots:
        candidate_roots.extend(target_roots)

    for root in candidate_roots:
        if not os.path.isdir(root):
            continue
        abs_root = os.path.abspath(root)
        try:
            rel = os.path.relpath(abs_script_dir, abs_root)
        except ValueError:
            continue
        if not rel.startswith("..") and rel != ".":
            return os.path.abspath(os.path.join(abs_output_dir, rel))
        if rel == ".":
            return abs_output_dir

    return abs_output_dir


def resolve_static_save_target(
    script_path: str,
    call_file: str | None,
    call_format: str | None,
    *,
    output_file: str | None = None,
    output_dir: str | None = None,
    image_format: str | None = None,
    current_target_root: str = "",
    target_roots: Sequence[str] = (),
) -> str:
    """Resolve the output file path that a static `save(file, format)` call in `script_path` will write."""
    eff_format = image_format if image_format else call_format
    if output_file is not None:
        target = os.path.abspath(output_file)
        if eff_format:
            stem, _ = os.path.splitext(target)
            target = f"{stem}.{eff_format}"
        return os.path.abspath(target)

    effective_output_dir = resolve_effective_output_dir(
        output_dir=output_dir,
        script_path=script_path,
        current_target_root=current_target_root,
        target_roots=target_roots,
    )
    if call_file is None:
        ext = eff_format or "png"
        target_dir = (
            effective_output_dir if effective_output_dir is not None else os.path.dirname(os.path.abspath(script_path))
        )
        stem = os.path.splitext(os.path.basename(script_path))[0]
        return os.path.abspath(os.path.join(target_dir, f"{stem}.{ext}"))

    eff_file = f"{os.path.splitext(call_file)[0]}.{eff_format}" if eff_format else call_file
    if effective_output_dir is not None and not os.path.isabs(eff_file):
        return os.path.abspath(os.path.join(effective_output_dir, eff_file))
    if os.path.isabs(eff_file):
        return os.path.abspath(eff_file)
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(script_path)), eff_file))


def check_duplicate_script_outputs(
    file_paths: Sequence[str],
    display_names: Sequence[str],
    resolve_target_fn: Callable[[str, str | None, str | None], str],
) -> dict[str, int]:
    """Pre-check target Python scripts via AST for duplicate output image paths and count saves per file."""
    seen_outputs: dict[str, str] = {}
    save_counts: dict[str, int] = {}
    for file_path, disp_name in zip(file_paths, display_names):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=file_path)
        except (OSError, SyntaxError) as exc:
            logger.debug(f"Skipping static AST check for {file_path}: {exc}")
            save_counts[file_path] = 0
            continue

        visitor = _SaveCallVisitor()
        visitor.visit(tree)
        for call_file, call_format, lineno in visitor.static_saves:
            target_abs = resolve_target_fn(file_path, call_file, call_format)
            src_label = f"{disp_name} (line {lineno})"
            if target_abs in seen_outputs:
                raise ValueError(format_duplicate_output_error(target_abs, seen_outputs[target_abs], src_label))
            seen_outputs[target_abs] = src_label
        save_counts[file_path] = visitor.save_count
    return save_counts


def _get_python_files(directory: str) -> list[str]:
    """Retrieve all Python files recursively within the specified directory."""
    python_files: list[str] = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.startswith("."):
                continue
            if file in {"styles.py", "utils.py", "__init__.py"}:
                continue
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                python_files.append(file_path)

    def sort_key(path: str) -> tuple[int, str]:
        return (path.count(os.sep), path)

    return sorted(python_files, key=sort_key)


def _collect_target_files(
    target_list: Sequence[str],
    executer: DrawlibExecuter | None = None,
) -> tuple[list[str], list[str], list[str]]:
    """Resolve valid target paths and collect all Python and Markdown files across those targets."""
    resolved_targets: list[str] = []
    all_py_files: list[str] = []
    all_md_files: list[str] = []
    get_py_fn = executer._get_python_files if executer is not None else _get_python_files
    for target_file in target_list:
        if not os.path.isfile(target_file) and not os.path.isdir(target_file):
            logger.warning(f'ignore arg "{target_file}" since it is not a file/dir path')
            continue
        realpath = os.path.realpath(os.path.abspath(target_file))
        resolved_targets.append(realpath)
        if os.path.isfile(realpath):
            if realpath.endswith(".py"):
                all_py_files.append(realpath)
            elif realpath.lower().endswith((".md", ".markdown")):
                all_md_files.append(realpath)
        elif os.path.isdir(realpath):
            all_py_files.extend(fp for fp in get_py_fn(realpath) if not os.path.basename(fp).startswith("__"))
            for root, dirnames, files in os.walk(realpath):
                dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and not d.startswith("_"))
                for f in sorted(files):
                    if f.startswith(".") or f.startswith("_"):
                        continue
                    f_lower = f.lower()
                    if (
                        f_lower.endswith((".md", ".markdown"))
                        and not f_lower.startswith("readme")
                        and f_lower not in {"navbar.md", "navbar.markdown", "output_readme.md", "output_html_readme.md"}
                    ):
                        all_md_files.append(os.path.join(root, f))
    return resolved_targets, all_py_files, all_md_files


def _normalize_build_inputs_and_output(
    target_list: Sequence[str],
    output: str | None,
) -> tuple[list[str], str | None, str | None]:
    """Normalize input targets and resolve output directory/file destinations."""
    targets = list(target_list)
    if len(targets) == 1 and os.path.isdir(targets[0]) and output is None:
        candidate_codes = os.path.join(targets[0], "codes")
        candidate_images = os.path.join(targets[0], "images")
        if os.path.isdir(candidate_codes):
            targets = [candidate_codes]
            output = candidate_images

    output_dir: str | None = None
    output_file: str | None = None
    if output:
        ext = os.path.splitext(output)[1].lower()
        is_single = len(targets) == 1 and os.path.isfile(targets[0])
        if is_single and ext in {".png", ".webp", ".jpg", ".jpeg", ".pdf"} and not os.path.isdir(output):
            output_file = output
        else:
            output_dir = output

    return targets, output_dir, output_file


def _resolve_execution_mode(
    disable_auto_clear: bool,
    enable_auto_initialize: bool,
) -> Literal["none", "auto_clear", "auto_initialize"]:
    """Resolve canvas execution mode from CLI flags."""
    if disable_auto_clear:
        return "none"
    if enable_auto_initialize:
        return "auto_initialize"
    return "auto_clear"
