# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Original Code icons."""

from pathlib import Path

from drawlib._icons.png_icons.original_code._base import (
    ORIGINAL_CODE_ALIASES,
    ORIGINAL_CODE_PROVIDER,
)
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, OriginalCodeIcon
from drawlib.icons import original_code
from drawlib.styles import Styles
from drawlib.types import Style


class TestOriginalCodeIcons:
    """Tests for `drawlib.icons.original_code` and `OriginalCodeIcon`."""

    def test_original_code_all_icons(self, tmp_path: Path) -> None:
        """Verify all 96 canonical icons (24 concepts + 72 brands) and 91 aliases exist and render."""
        clear()
        canonical_96 = [
            "source_code",
            "sdk_library",
            "package_module",
            "cli_tool",
            "ide_editor",
            "rest_api",
            "graphql_api",
            "rpc_call",
            "websocket",
            "webhook",
            "microservice",
            "monolith",
            "serverless_func",
            "background_worker",
            "cron_job",
            "compiler_build",
            "runtime_vm",
            "unit_test",
            "debugger",
            "linter_formatter",
            "json_schema",
            "xml_markup",
            "binary_executable",
            "regex_parser",
            "python",
            "fastapi",
            "django",
            "flask",
            "uvicorn",
            "uv",
            "poetry",
            "pypi",
            "pydantic",
            "sqlalchemy",
            "celery",
            "pytest",
            "numpy",
            "pandas",
            "javascript",
            "typescript",
            "nodejs",
            "deno",
            "bun",
            "react",
            "nextjs",
            "vuejs",
            "nuxt",
            "angular",
            "svelte",
            "astro",
            "htmx",
            "jquery",
            "tailwind_css",
            "vite",
            "nestjs",
            "express",
            "hono",
            "prisma",
            "npm",
            "go",
            "gin",
            "echo",
            "java",
            "kotlin",
            "spring",
            "gradle",
            "rust",
            "cargo",
            "tokio",
            "csharp",
            "dotnet",
            "blazor",
            "php",
            "laravel",
            "ruby",
            "rails",
            "c",
            "cpp",
            "bash",
            "swift",
            "dart",
            "flutter",
            "react_native",
            "html5",
            "css3",
            "webassembly",
            "graphql",
            "grpc",
            "openapi",
            "protobuf",
            "firebase",
            "colab",
            "antigravity",
            "android_studio",
            "vscode",
            "intellij",
        ]
        assert len(canonical_96) == 96
        for idx, name in enumerate(canonical_96):
            assert hasattr(original_code, name), f"Missing canonical icon: {name}"
            assert hasattr(OriginalCodeIcon, name.upper()), f"Missing enum: {name.upper()}"
            col = idx % 12
            row = idx // 12
            fn = getattr(original_code, name)
            fn(xy=(8 + col * 7.5, 90 - row * 11), width=6, style=Style(), variant="default")

        assert len(ORIGINAL_CODE_ALIASES) == 91
        for alias in ORIGINAL_CODE_ALIASES:
            assert hasattr(original_code, alias), f"Missing alias function: {alias}"
            assert hasattr(OriginalCodeIcon, alias.upper()), f"Missing alias enum: {alias.upper()}"

        out = tmp_path / "test_original_code_all.png"
        save(str(out))
        assert out.is_file()

    def test_original_code_aliases(self, tmp_path: Path) -> None:
        """Verify shorthand aliases resolve to canonical original_code icons."""
        clear()
        original_code.code_file(xy=(15, 70), width=10, style=Style())
        original_code.http_api(xy=(30, 70), width=10, style=Style())
        original_code.py(xy=(45, 70), width=10, style=Style())
        original_code.ts(xy=(60, 70), width=10, style=Style())
        original_code.golang(xy=(75, 70), width=10, style=Style())
        original_code.google_colab(xy=(90, 70), width=10, style=Style())
        original_code.vs_code(xy=(15, 45), width=10, style=Style())
        original_code.lambda_func(xy=(30, 45), width=10, style=Style())

        out = tmp_path / "test_original_code_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_original_code_architecture_enum(self, tmp_path: Path) -> None:
        """Verify OriginalCodeIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("React", width=20, height=20, icon=OriginalCodeIcon.REACT), (20, 50))
        n2 = diag.add(
            Node("REST API", width=20, height=20, icon=OriginalCodeIcon.REST_API),
            (50, 50),
        )
        n3 = diag.add(Node("Python", width=20, height=20, icon=OriginalCodeIcon.PYTHON), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_original_code.png"
        save(str(out))
        assert out.is_file()

    def test_original_code_provider_metadata(self) -> None:
        """Verify provider package name and aliases mapping."""
        assert ORIGINAL_CODE_PROVIDER.name == "original_code"
        assert ORIGINAL_CODE_PROVIDER.package_name == "icon_original_code"
        assert ORIGINAL_CODE_PROVIDER.asset_subdir == "icons/original_code"
        assert ORIGINAL_CODE_PROVIDER.aliases["py"] == "python"
        assert ORIGINAL_CODE_PROVIDER.aliases["http_api"] == "rest_api"
        assert ORIGINAL_CODE_PROVIDER.aliases["google_colab"] == "colab"
