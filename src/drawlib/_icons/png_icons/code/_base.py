# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Code (languages, frameworks, APIs, IDEs) icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

CODE_ALIASES: dict[str, str] = {
    "apollo_graphql": "apollo",
    "aspnet": "dotnet",
    "c_lang": "c",
    "cplusplus": "cpp",
    "cs": "csharp",
    "css": "css3",
    "echo_go": "echo",
    "elixir_lang": "elixir",
    "expressjs": "express",
    "gin_gonic": "gin",
    "golang": "go",
    "google_colab": "colab",
    "gql": "graphql",
    "html": "html5",
    "jetbrains": "intellij",
    "js": "javascript",
    "julia_lang": "julia",
    "jvm": "java",
    "kt": "kotlin",
    "lua_lang": "lua",
    "nest": "nestjs",
    "net": "dotnet",
    "next": "nextjs",
    "node": "nodejs",
    "nuxtjs": "nuxt",
    "openjdk": "java",
    "proto": "protobuf",
    "py": "python",
    "r_lang": "r",
    "rb": "ruby",
    "reactjs": "react",
    "rn": "react_native",
    "rs": "rust",
    "ruby_on_rails": "rails",
    "scala_lang": "scala",
    "sh": "bash",
    "shell": "bash",
    "sol": "solidity",
    "spring_boot": "spring",
    "swagger": "openapi",
    "tailwind": "tailwind_css",
    "ts": "typescript",
    "vitejs": "vite",
    "vs_code": "vscode",
    "vue": "vuejs",
    "wasm": "webassembly",
    "zig_lang": "zig",
}

CODE_PROVIDER = PngIconProvider(
    name="code",
    package_name="icon_code",
    asset_subdir="icons/code",
    aliases=CODE_ALIASES,
)

_write = CODE_PROVIDER.write
