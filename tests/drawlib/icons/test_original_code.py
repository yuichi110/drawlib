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
        """Verify all 121 canonical icons (24 concepts + 97 brands) exist and render."""
        clear()
        canonical_121 = [
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
            "scala",
            "elixir",
            "zig",
            "lua",
            "r",
            "julia",
            "solidity",
            "sql",
            "apollo",
            "hasura",
            "trpc",
            "axum",
            "quarkus",
            "pocketbase",
            "appwrite",
            "convex",
            "remix",
            "tauri",
            "electron",
            "expo",
            "pnpm",
            "yarn",
            "biome",
            "vitest",
            "storybook",
        ]
        assert len(canonical_121) == 121
        for idx, name in enumerate(canonical_121):
            assert hasattr(original_code, name), f"Missing canonical icon: {name}"
            assert hasattr(OriginalCodeIcon, name.upper()), f"Missing enum: {name.upper()}"
            col = idx % 13
            row = idx // 13
            fn = getattr(original_code, name)
            fn(xy=(6 + col * 7.2, 92 - row * 9.0), width=5.5, style=Style(), variant="default")

        out = tmp_path / "test_original_code_all.png"
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
        """Verify provider package name."""
        assert ORIGINAL_CODE_PROVIDER.name == "original_code"
        assert ORIGINAL_CODE_PROVIDER.package_name == "icon_original_code"
        assert ORIGINAL_CODE_PROVIDER.asset_subdir == "icons/original_code"
