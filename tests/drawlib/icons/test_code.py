# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Code icons."""

from pathlib import Path

from drawlib._icons.png_icons.code._base import CODE_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, CodeIcon, Node
from drawlib.icons import code
from drawlib.styles import Styles
from drawlib.types import Style


class TestCodeIcons:
    """Tests for official Code icon provider and diagram enum."""

    def test_code_all_icons(self, tmp_path: Path) -> None:
        """Verify all 72 official language, framework, API, and IDE icons render cleanly."""
        clear()
        names = [
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
        for idx, name in enumerate(names):
            col = idx % 12
            row = idx // 12
            fn = getattr(code, name)
            fn(xy=(8 + col * 7.5, 85 - row * 14), width=6, style=Style(), variant="default")

        out = tmp_path / "test_code_all.png"
        save(str(out))
        assert out.is_file()

    def test_code_aliases(self, tmp_path: Path) -> None:
        """Verify shorthand aliases resolve to canonical code icons."""
        clear()
        code.py(xy=(15, 70), width=10, style=Style())
        code.ts(xy=(30, 70), width=10, style=Style())
        code.js(xy=(45, 70), width=10, style=Style())
        code.golang(xy=(60, 70), width=10, style=Style())
        code.rs(xy=(75, 70), width=10, style=Style())
        code.google_colab(xy=(90, 70), width=10, style=Style())
        code.vs_code(xy=(15, 45), width=10, style=Style())
        code.spring_boot(xy=(30, 45), width=10, style=Style())

        out = tmp_path / "test_code_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_code_architecture_enum(self, tmp_path: Path) -> None:
        """Verify CodeIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("React", width=20, height=20, icon=CodeIcon.REACT), (20, 50))
        n2 = diag.add(Node("FastAPI", width=20, height=20, icon=CodeIcon.FASTAPI), (50, 50))
        n3 = diag.add(Node("Go", width=20, height=20, icon=CodeIcon.GO), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_code.png"
        save(str(out))
        assert out.is_file()

    def test_code_provider_metadata(self) -> None:
        """Verify provider package name and aliases mapping."""
        assert CODE_PROVIDER.name == "code"
        assert CODE_PROVIDER.package_name == "icon_code"
        assert CODE_PROVIDER.aliases["py"] == "python"
        assert CODE_PROVIDER.aliases["ts"] == "typescript"
        assert CODE_PROVIDER.aliases["google_colab"] == "colab"
