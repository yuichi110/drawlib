# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""SourceCode smart art implementation module.

Provides syntax-highlighted source code container rendering using vector graphics primitives
and the Pygments lexical analyzer.
"""

from __future__ import annotations

import contextlib
import os
from dataclasses import dataclass
from typing import Any

import pygments
from pydantic import validate_call
from pygments.lexer import Lexer
from pygments.lexers import (
    get_lexer_by_name,
    get_lexer_for_filename,
    guess_lexer,
)
from pygments.lexers.special import TextLexer
from pygments.token import Token

from drawlib._core.l1_core import get_script_relative_path
from drawlib._core.l2_types import Coordinate, FilePath, FontBase, FontFile, PosFloat
from drawlib._core.l3_fonts import FontSourceCode
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import TextUtil, canvas, rectangle, text


@dataclass
class SourceCodeStyles:
    """Source code rendering style configuration.

    Attributes:
        box_style: Style for the outer code container card.
        linenum_style: Style for line numbers in the gutter.
        default: Style for default code text and unclassified identifiers.
        keyword: Style for control keywords (e.g. def, class, return, if).
        string: Style for string literals.
        comment: Style for comments.
        number: Style for numeric literals.
        function: Style for function and method definitions/calls.
        type_: Style for classes, types, and builtin identifiers.
        operator: Style for operators and punctuation symbols.
    """

    box_style: Style
    linenum_style: Style
    default: Style
    keyword: Style
    string: Style
    comment: Style
    number: Style
    function: Style
    type_: Style
    operator: Style

    def patch(
        self,
        *,
        box_style: Style | None = None,
        linenum_style: Style | None = None,
        default: Style | None = None,
        keyword: Style | None = None,
        string: Style | None = None,
        comment: Style | None = None,
        number: Style | None = None,
        function: Style | None = None,
        type_: Style | None = None,
        type: Style | None = None,
        operator: Style | None = None,
        text_size: float | None = None,
    ) -> SourceCodeStyles:
        """Create a new SourceCodeStyles instance with specified styles updated.

        Args:
            box_style: Optional updated box style.
            linenum_style: Optional updated line number style.
            default: Optional updated default text style.
            keyword: Optional updated keyword style.
            string: Optional updated string literal style.
            comment: Optional updated comment style.
            number: Optional updated number style.
            function: Optional updated function style.
            type_: Optional updated type/class style.
            type: Alias for type_.
            operator: Optional updated operator style.
            text_size: Optional updated font size applied to all text styles.

        Returns:
            SourceCodeStyles: A new instance with patched styles.
        """
        resolved_type = type if type is not None else type_
        b_style = box_style.model_copy() if box_style is not None else self.box_style.model_copy()
        ln_style = linenum_style.model_copy() if linenum_style is not None else self.linenum_style.model_copy()
        d_style = default.model_copy() if default is not None else self.default.model_copy()
        k_style = keyword.model_copy() if keyword is not None else self.keyword.model_copy()
        s_style = string.model_copy() if string is not None else self.string.model_copy()
        c_style = comment.model_copy() if comment is not None else self.comment.model_copy()
        n_style = number.model_copy() if number is not None else self.number.model_copy()
        f_style = function.model_copy() if function is not None else self.function.model_copy()
        t_style = resolved_type.model_copy() if resolved_type is not None else self.type_.model_copy()
        op_style = operator.model_copy() if operator is not None else self.operator.model_copy()

        if text_size is not None:
            ln_style = ln_style.patch(text_size=text_size)
            d_style = d_style.patch(text_size=text_size)
            k_style = k_style.patch(text_size=text_size)
            s_style = s_style.patch(text_size=text_size)
            c_style = c_style.patch(text_size=text_size)
            n_style = n_style.patch(text_size=text_size)
            f_style = f_style.patch(text_size=text_size)
            t_style = t_style.patch(text_size=text_size)
            op_style = op_style.patch(text_size=text_size)

        return SourceCodeStyles(
            box_style=b_style,
            linenum_style=ln_style,
            default=d_style,
            keyword=k_style,
            string=s_style,
            comment=c_style,
            number=n_style,
            function=f_style,
            type_=t_style,
            operator=op_style,
        )

    @classmethod
    def get(
        cls,
        styles: str = "default",
        font_lang: str = "en",
        *,
        font: FontSourceCode | FontFile | None = None,
        text_size: float = 12.0,
    ) -> SourceCodeStyles:
        """Create a SourceCodeStyles instance based on theme and language.

        Args:
            styles: Theme name ('default', 'monochrome', 'dark', 'monokai', 'google').
            font_lang: Natural language code ('en', 'ja', 'zh-cn', 'ko', etc.) for font selection.
            font: Optional font override. If None, font is resolved from font_lang.
            text_size: Base font size for code and line numbers.

        Returns:
            SourceCodeStyles: Preconfigured style model.
        """
        if font is not None:
            resolved_font: FontBase | FontFile = font
        elif font_lang in {"ja", "zh-cn", "zh-tw", "ko"}:
            resolved_font = FontSourceCode.SOURCEHANCODEJP
        else:
            resolved_font = FontSourceCode.SOURCECODEPRO

        theme = styles.lower().strip()
        if theme == "monochrome":
            return cls._get_monochrome(resolved_font, text_size)
        if theme in {"dark", "monokai", "github-dark"}:
            return cls._get_dark(resolved_font, text_size)
        if theme == "google":
            return cls._get_google(resolved_font, text_size)
        return cls._get_default(resolved_font, text_size)

    @classmethod
    def _get_default(cls, font: FontBase | FontFile, text_size: float) -> SourceCodeStyles:
        return cls(
            box_style=Style(
                shape_fill_color=(248, 250, 252),
                shape_line_color=(203, 213, 225),
                shape_line_width=1.0,
            ),
            linenum_style=Style(
                text_color=(148, 163, 184),
                text_font=font,
                text_size=text_size,
                text_halign="right",
                text_valign="center",
            ),
            default=Style(
                text_color=(15, 23, 42),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            keyword=Style(
                text_color=(37, 99, 235),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            string=Style(
                text_color=(22, 163, 74),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            comment=Style(
                text_color=(100, 116, 139),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            number=Style(
                text_color=(217, 119, 6),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            function=Style(
                text_color=(220, 38, 38),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            type_=Style(
                text_color=(147, 51, 234),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            operator=Style(
                text_color=(71, 85, 105),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
        )

    @classmethod
    def _get_monochrome(cls, font: FontBase | FontFile, text_size: float) -> SourceCodeStyles:
        return cls(
            box_style=Style(
                shape_fill_color=(255, 255, 255),
                shape_line_color=(0, 0, 0),
                shape_line_width=1.0,
            ),
            linenum_style=Style(
                text_color=(150, 150, 150),
                text_font=font,
                text_size=text_size,
                text_halign="right",
                text_valign="center",
            ),
            default=Style(
                text_color=(0, 0, 0),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            keyword=Style(
                text_color=(0, 0, 0),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            string=Style(
                text_color=(80, 80, 80),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            comment=Style(
                text_color=(130, 130, 130),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            number=Style(
                text_color=(60, 60, 60),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            function=Style(
                text_color=(0, 0, 0),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            type_=Style(
                text_color=(40, 40, 40),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            operator=Style(
                text_color=(100, 100, 100),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
        )

    @classmethod
    def _get_dark(cls, font: FontBase | FontFile, text_size: float) -> SourceCodeStyles:
        return cls(
            box_style=Style(
                shape_fill_color=(39, 40, 34),
                shape_line_color=(60, 60, 60),
                shape_line_width=1.0,
            ),
            linenum_style=Style(
                text_color=(120, 120, 120),
                text_font=font,
                text_size=text_size,
                text_halign="right",
                text_valign="center",
            ),
            default=Style(
                text_color=(248, 248, 242),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            keyword=Style(
                text_color=(249, 38, 114),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            string=Style(
                text_color=(230, 219, 116),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            comment=Style(
                text_color=(117, 113, 94),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            number=Style(
                text_color=(174, 129, 255),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            function=Style(
                text_color=(166, 226, 46),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            type_=Style(
                text_color=(102, 217, 239),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            operator=Style(
                text_color=(249, 38, 114),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
        )

    @classmethod
    def _get_google(cls, font: FontBase | FontFile, text_size: float) -> SourceCodeStyles:
        return cls(
            box_style=Style(
                shape_fill_color=(255, 255, 255),
                shape_line_color=(218, 220, 224),
                shape_line_width=1.0,
            ),
            linenum_style=Style(
                text_color=(128, 134, 139),
                text_font=font,
                text_size=text_size,
                text_halign="right",
                text_valign="center",
            ),
            default=Style(
                text_color=(32, 33, 36),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            keyword=Style(
                text_color=(26, 115, 232),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            string=Style(
                text_color=(30, 142, 62),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            comment=Style(
                text_color=(128, 134, 139),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            number=Style(
                text_color=(249, 171, 0),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            function=Style(
                text_color=(217, 48, 37),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            type_=Style(
                text_color=(175, 56, 196),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
            operator=Style(
                text_color=(95, 99, 104),
                text_font=font,
                text_size=text_size,
                text_halign="left",
                text_valign="center",
            ),
        )


class SourceCode:
    """Class for rendering syntax-highlighted source code as vector graphics.

    This class provides static and class methods to draw code directly on the canvas
    without maintaining stateful instance instances.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """Raise TypeError to enforce classmethod usage."""
        raise TypeError(
            "SourceCode cannot be instantiated directly. "
            "Use 'SourceCode.draw(xy, width, styles=..., ...)' instead."
        )

    @classmethod
    @validate_call
    def draw(  # noqa: C901
        cls,
        xy: Coordinate,
        width: PosFloat,
        code: str | None = None,
        *,
        styles: SourceCodeStyles,
        file: FilePath | None = None,
        code_lang: str | None = None,
        show_linenum: bool = False,
        r: PosFloat = 1.5,
    ) -> None:
        """Draw syntax-highlighted source code on the canvas.

        Args:
            xy: Top-left coordinate (x, y) of the code container.
            width: Total width of the code container.
            code: Source code string to render. (Alternative to `file`).
            styles: Required SourceCodeStyles defining token colors and fonts.
            file: Path to a file containing source code. (Alternative to `code`).
            code_lang: Programming language for highlighting (e.g. 'python', 'json').
                       If None, language is inferred from `file` or code content.
            show_linenum: Whether to display line numbers in a gutter.
            r: Corner radius of the container box. Defaults to 1.5.

        Raises:
            ValueError: If neither or both `code` and `file` are provided.
        """
        if code is None and file is None:
            raise ValueError("Either 'code' or 'file' must be specified.")
        if code is not None and file is not None:
            raise ValueError("Cannot specify both 'code' and 'file'.")

        if file is not None:
            code_str = cls.get_text(file, strip=False)
        elif code is not None:
            code_str = code
        else:
            raise ValueError("Either 'code' or 'file' must be specified.")

        code_str = code_str.rstrip("\r\n")
        lexer = cls._get_lexer(code_lang, code_str, file)

        # Lex tokens and partition into lines
        tokens = list(pygments.lex(code_str, lexer))
        token_lines: list[list[tuple[Any, str]]] = []
        current_line: list[tuple[Any, str]] = []
        for tok_type, tok_val in tokens:
            parts = tok_val.split("\n")
            for idx, part in enumerate(parts):
                if idx > 0:
                    token_lines.append(current_line)
                    current_line = []
                if part:
                    current_line.append((tok_type, part))
        if current_line or not token_lines:
            token_lines.append(current_line)

        # Ensure canvas is initialized and axes margins removed for exact pixel math
        canvas._remove_margin()
        canvas._fig.canvas.draw()
        fig_canvas = canvas._fig.canvas
        renderer: Any = getattr(fig_canvas, "get_renderer")()
        inv = canvas._ax.transData.inverted()

        width_cache: dict[tuple[str, str, float], float] = {}

        def get_dx(s: str, style_obj: Style) -> float:
            if not s:
                return 0.0
            prop = TextUtil.get_font_properties(style_obj)
            file_name = str(prop.get_file() or "")
            size_val = float(prop.get_size())
            key: tuple[str, str, float] = (s, file_name, size_val)
            if key in width_cache:
                return width_cache[key]
            w_px, _, _ = renderer.get_text_width_height_descent(s, prop, False)
            p0 = inv.transform((0, 0))
            p1 = inv.transform((w_px, 0))
            dx = float(p1[0] - p0[0])
            width_cache[key] = dx
            return dx

        # Layout metrics
        text_size: float = float(styles.default.text_size or 12.0)
        pt_to_canvas = float(canvas._width) / 720.0
        font_size_canvas = text_size * pt_to_canvas
        line_height = font_size_canvas * 1.8
        pad_x = font_size_canvas * 1.5
        pad_y = font_size_canvas * 1.2

        num_lines = len(token_lines)
        if show_linenum:
            digits = max(2, len(str(num_lines)))
            gutter_w = get_dx("9" * digits + " ", styles.linenum_style)
        else:
            gutter_w = 0.0

        box_h = pad_y * 2.0 + num_lines * line_height

        # Draw outer container rectangle
        cx = xy[0] + width / 2.0
        cy = xy[1] - box_h / 2.0
        rectangle(
            xy=(cx, cy),
            width=width,
            height=box_h,
            r=r,
            style=styles.box_style,
        )

        # Draw line numbers
        if show_linenum:
            line_num_style = styles.linenum_style.patch(text_halign="right", text_valign="center")
            for i in range(num_lines):
                line_y = xy[1] - pad_y - (i + 0.5) * line_height
                line_str = f"{i + 1} "
                num_x = xy[0] + pad_x + gutter_w
                text(
                    xy=(num_x, line_y),
                    text=line_str,
                    style=line_num_style,
                )

        # Draw syntax-highlighted code tokens
        code_start_x = xy[0] + pad_x + gutter_w + (get_dx(" ", styles.default) if show_linenum else 0.0)
        for i, line_toks in enumerate(token_lines):
            line_y = xy[1] - pad_y - (i + 0.5) * line_height
            token_x = code_start_x
            for tok_type, tok_val in line_toks:
                tok_style = cls._map_token_to_style(tok_type, styles)
                tok_style = tok_style.patch(text_halign="left", text_valign="center")
                text(
                    xy=(token_x, line_y),
                    text=tok_val,
                    style=tok_style,
                )
                token_x += get_dx(tok_val, tok_style)

    @staticmethod
    @validate_call
    def get_text(file: FilePath, strip: bool = True) -> str:
        """Retrieve source code text from a file.

        Args:
            file: Path to the file. If a relative path is provided,
                  it is resolved relative to the caller script directory.
            strip: Whether to strip leading and trailing whitespace.

        Returns:
            str: Contents of the file.

        Raises:
            ValueError: If the file does not exist.
        """
        try:
            resolved = get_script_relative_path(file) if not os.path.isabs(file) else file
        except FileNotFoundError:
            resolved = os.path.abspath(file)

        if not os.path.isfile(resolved):
            raise ValueError(f'File "{file}" does not exist.')

        with open(resolved, "r", encoding="utf8") as fin:
            content = fin.read()

        if strip:
            content = content.strip()
        return content

    @staticmethod
    def _get_lexer(code_lang: str | None, code: str, file: str | None) -> Lexer:
        if code_lang is not None:
            if code_lang in {"none", "plain", "text"}:
                return TextLexer()
            return get_lexer_by_name(code_lang)

        if file is not None:
            with contextlib.suppress(Exception):
                return get_lexer_for_filename(file, code)

        with contextlib.suppress(Exception):
            return guess_lexer(code)
        return TextLexer()

    @staticmethod
    def _map_token_to_style(token_type: Any, styles: SourceCodeStyles) -> Style:  # noqa: ANN401
        mappings: tuple[tuple[Any, Style], ...] = (
            (Token.Keyword, styles.keyword),
            (Token.String, styles.string),
            (Token.Comment, styles.comment),
            (Token.Number, styles.number),
            (Token.Name.Function, styles.function),
            ({Token.Name.Class, Token.Name.Builtin}, styles.type_),
            ({Token.Operator, Token.Punctuation}, styles.operator),
        )
        for pattern, style_val in mappings:
            if isinstance(pattern, set):
                if any(token_type in p for p in pattern):
                    return style_val
            elif token_type in pattern:
                return style_val
        return styles.default


@validate_call
def sourcecode(
    xy: Coordinate,
    width: PosFloat,
    code: str | None = None,
    *,
    styles: SourceCodeStyles,
    file: FilePath | None = None,
    code_lang: str | None = None,
    show_linenum: bool = False,
    r: PosFloat = 1.5,
) -> None:
    """Draw syntax-highlighted source code on the canvas.

    Function alias for `SourceCode.draw()`.

    Args:
        xy: Top-left coordinate (x, y) of the code container.
        width: Total width of the code container.
        code: Source code string to render. (Alternative to `file`).
        styles: Required SourceCodeStyles defining token colors and fonts.
        file: Path to a file containing source code. (Alternative to `code`).
        code_lang: Programming language for highlighting (e.g. 'python', 'json').
        show_linenum: Whether to display line numbers.
        r: Corner radius of the container box. Defaults to 1.5.
    """
    SourceCode.draw(
        xy=xy,
        width=width,
        code=code,
        styles=styles,
        file=file,
        code_lang=code_lang,
        show_linenum=show_linenum,
        r=r,
    )


def get_source_code_styles(
    styles: str = "default",
    font_lang: str = "en",
    *,
    font: FontSourceCode | FontFile | None = None,
    text_size: float = 12.0,
) -> SourceCodeStyles:
    """Get SourceCodeStyles configured for a theme and language.

    Function alias for `SourceCodeStyles.get()`.

    Args:
        styles: Theme name ('default', 'monochrome', 'dark', 'monokai', 'google').
        font_lang: Natural language code ('en', 'ja', 'zh-cn', 'ko', etc.) for font selection.
        font: Optional font override. If None, font is resolved from font_lang.
        text_size: Base font size for code and line numbers.

    Returns:
        SourceCodeStyles: Configured style model.
    """
    return SourceCodeStyles.get(
        styles=styles,
        font_lang=font_lang,
        font=font,
        text_size=text_size,
    )
