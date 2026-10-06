# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Tests for doc_builder syntax highlighting module."""

from __future__ import annotations

from pygments.lexers.python import PythonLexer
from pygments.lexers.special import TextLexer

from drawlib._builder.doc_builder.highlight import pygments_highlight, resolve_lexer
from drawlib._builder.doc_builder.parser_md import parse_markdown_to_html


def test_resolve_lexer_known_language() -> None:
    lexer = resolve_lexer("python", "print('hello')")
    assert isinstance(lexer, PythonLexer)


def test_resolve_lexer_plain_text() -> None:
    for lang in ("none", "plain", "text", "txt", "NONE", "  plain  "):
        lexer = resolve_lexer(lang, "some plain text")
        assert isinstance(lexer, TextLexer)


def test_resolve_lexer_guess_python() -> None:
    code = "def sample_function(x, y):\n    return x + y\n"
    lexer = resolve_lexer(None, code)
    # Pygments guess_lexer resolves python code or text
    assert lexer is not None


def test_resolve_lexer_unknown_language_fallback() -> None:
    lexer = resolve_lexer("unknown_nonexistent_lang_xyz", "just normal text")
    assert isinstance(lexer, TextLexer)


def test_pygments_highlight_empty_code() -> None:
    assert pygments_highlight("") == ""


def test_pygments_highlight_python() -> None:
    code = "def add(a, b):\n    return a + b"
    html = pygments_highlight(code, "python")
    assert '<span class="k">def</span>' in html
    assert '<span class="nf">add</span>' in html
    assert '<span class="k">return</span>' in html


def test_parse_markdown_to_html_syntax_highlight() -> None:
    md_text = """# Hello

```python
def greet(name):
    return f"Hello, {name}!"
```
"""
    result = parse_markdown_to_html(md_text)
    assert '<pre><code class="language-python">' in result
    assert '<span class="k">def</span>' in result
    assert '<span class="nf">greet</span>' in result


def test_parse_markdown_to_html_plain_block() -> None:
    md_text = """```text
Plain log message without highlight
```"""
    result = parse_markdown_to_html(md_text)
    assert '<pre><code class="language-text">' in result
    assert "Plain log message without highlight" in result
