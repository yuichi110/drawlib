# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Syntax highlighting module using Pygments for markdown-it-py compilation."""

from __future__ import annotations

import contextlib

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexer import Lexer
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.lexers.special import TextLexer


def resolve_lexer(code_lang: str | None, code: str) -> Lexer:
    """Resolve Pygments lexer safely for code highlighting.

    Args:
        code_lang (str | None): Language name or identifier (e.g. 'python', 'bash').
        code (str): Source code string to highlight or guess from.

    Returns:
        Lexer: Pygments lexer instance (falls back to TextLexer if unresolved).
    """
    if code_lang:
        lang_clean = code_lang.strip().lower()
        if lang_clean in {"none", "plain", "text", "txt"}:
            return TextLexer()
        with contextlib.suppress(Exception):
            return get_lexer_by_name(lang_clean)

    if code.strip():
        with contextlib.suppress(Exception):
            return guess_lexer(code)

    return TextLexer()


def pygments_highlight(code: str, lang: str = "", attrs: str = "") -> str:
    """Highlight code block callback for markdown-it-py.

    Args:
        code (str): Raw source code string inside Markdown fence block.
        lang (str): Language identifier string (e.g. 'python', 'sh').
        attrs (str): Additional code block attributes (if any).

    Returns:
        str: Syntax-highlighted HTML snippet wrapped with spans, or empty string on fallback.
    """
    if not code:
        return ""

    try:
        lexer = resolve_lexer(lang, code)
        formatter = HtmlFormatter(nowrap=True)
        return highlight(code, lexer, formatter)
    except Exception:
        return ""
