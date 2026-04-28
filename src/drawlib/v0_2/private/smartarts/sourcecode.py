# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""SourceCode implementation module."""

import io
import os
from typing import Final, Literal, Optional, Tuple, Union

from PIL import Image
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexer import Lexer
from pygments.lexers import (
    get_lexer_by_name,
    guess_lexer,
)
from pygments.lexers.special import TextLexer
from pygments.styles import get_style_by_name

from drawlib.v0_2.private.core.dimage import Dimage
from drawlib.v0_2.private.core.fonts import FontFile, FontSourceCode
from drawlib.v0_2.private.core.model import ImageStyle
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.core.util import ColorUtil
from drawlib.v0_2.private.core_canvas.canvas import image
from drawlib.v0_2.private.download import download_if_not_exist
from drawlib.v0_2.private.util import error_handler, get_script_relative_path

PYGMENTS_LINENUM_TEXT_COLOR: Final[Tuple[int, int, int]] = (136, 136, 102)
PYGMENTS_LINENUM_BACKGROUND_COLOR: Final[Tuple[int, int, int]] = (238, 238, 221)


class SourceCode:
    """Class for rendering source code as an image using Pygments.

    This class allows you to configure the style and font of the rendered source code image.
    You can render the source code image using the `draw()` method or obtain the image
    directly with the `get_image()` method.
    """

    @error_handler
    def __init__(
        self,
        language: Optional[
            Literal[
                "bash",
                "c",
                "c#",
                "c++",
                "coffeescript",
                "css",
                "dart",
                "docker",
                "go",
                "groovy",
                "haskell",
                "html",
                "ini",
                "java",
                "javascript",
                "json",
                "julia",
                "kotlin",
                "less",
                "markdown",
                "none",
                "objective-c",
                "perl",
                "php",
                "plain",
                "powershell",
                "promql",
                "protobuf",
                "python",
                "restructuredtext",
                "ruby",
                "rust",
                "sql",
                "swift",
                "tex",
                "text",
                "toml",
                "typescript",
                "verilog",
                "xml",
                "yaml",
            ]
        ] = None,
        style: Literal[
            "bw",
            "sas",
            "staroffice",
            "xcode",
            "default",
            "monokai",
            "lightbulb",
            "github-dark",
            "rrt",
            # not recommended. but gray scale might be important
            "algol",
            "algol_nu",
            "friendly_grayscale",
        ] = "default",
        font: Union[
            FontSourceCode,
            FontFile,
            None,
        ] = None,
        show_linenum: bool = False,
        linenum_textcolor: Union[
            Tuple[int, int, int],
            Tuple[int, int, int, float],
        ] = PYGMENTS_LINENUM_TEXT_COLOR,
        linenum_bgcolor: Union[
            Tuple[int, int, int],
            Tuple[int, int, int, float],
        ] = PYGMENTS_LINENUM_BACKGROUND_COLOR,
    ) -> None:
        """Initialize the SourceCode renderer.

        Args:
            language (Optional[str]):
                    The programming language for syntax highlighting.
                    If None, the language will be guessed.
            style (str): The Pygments style to use for syntax highlighting.
                    Default is "default".
            font (Union[FontSourceCode, FontFile, None]):
                    The font to use for rendering the source code.
                    If None, a default font will be used.
            show_linenum (bool): Whether to show line numbers. Default is False.
            linenum_textcolor (Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
                    The color of the line numbers as an RGB or RGBA tuple.
                    Default is (136, 136, 102).
            linenum_bgcolor (Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
                    The background color of the line numbers as an RGB or RGBA tuple.
                    Default is (238, 238, 221).

        """
        self._lexer: Optional[Lexer] = self._get_lexer(language)
        self._formatter = self._get_formatter(style, font, show_linenum, linenum_textcolor, linenum_bgcolor)

    @error_handler
    def get_image(self, code: str) -> Dimage:
        """Generate an image of the source code.

        Args:
            code (str): The source code to render.

        Returns:
            Dimage: The generated image of the source code.

        """
        if self._lexer is None:
            lexer = guess_lexer(code)
        else:
            lexer = self._lexer

        # create image data
        image_buffer = io.BytesIO()
        highlight(code, lexer, self._formatter, image_buffer)
        image_buffer.seek(0)
        return Dimage(Image.open(image_buffer))

    @error_handler
    def draw(
        self,
        xy: Tuple[float, float],
        width: float,
        code: str,
        style: Optional[ImageStyle] = None,
    ) -> None:
        """Draw the source code image on a canvas.

        Args:
            xy (Tuple[float, float]): The (x, y) coordinates for the top-left corner of the image.
            width (float): The width of the image.
            code (str): The source code to render.
            style (Optional[ImageStyle]): The style to apply to the image.

        """
        image_ = self.get_image(code=code)
        image(xy=xy, width=width, image=image_, style=style)

    @staticmethod
    @error_handler
    def get_text(file: str, strip: bool = True) -> str:
        """Retrieve the text from a file.

        Args:
            file (str): The path to the file.
            strip (bool): Whether to strip leading and trailing whitespace.

        Returns:
            str: The contents of the file.

        """
        if not isinstance(file, str):
            raise ValueError('arg "file" must be str.')

        abspath = get_script_relative_path(file)
        if not os.path.isfile(abspath):
            raise ValueError(f'File "{file}" : "{abspath}" does not exist.')

        with open(abspath, "r", encoding="utf8") as fin:
            text = fin.read()

        if strip:
            text = text.strip()

        return text

    #
    # PRIVATE
    #

    @staticmethod
    def _get_lexer(language: Optional[str]) -> Optional[Lexer]:
        if language is None:
            # guess lexer at method draw()
            return None

        if language in {"none", "plain", "text"}:
            return TextLexer()

        return get_lexer_by_name(language)

    @staticmethod
    def _get_formatter(
        style: str,
        font: Union[FontFile, FontSourceCode, None],
        show_linenum: bool,
        linenum_textcolor: Union[
            Tuple[int, int, int],
            Tuple[int, int, int, float],
        ],
        linenum_bgcolor: Union[
            Tuple[int, int, int],
            Tuple[int, int, int, float],
        ],
    ) -> ImageFormatter:
        pygments_style = get_style_by_name(style)

        if font is None:
            file_path, download_url, md5_hash = dtheme.sourcecodefonts.get().value
            download_if_not_exist(
                file_path=file_path,
                download_url=download_url,
                md5_hash=md5_hash,
            )
        elif isinstance(font, FontFile):
            file_path = font.file
        elif isinstance(font, FontSourceCode):
            file_path, download_url, md5_hash = font.value
            download_if_not_exist(
                file_path=file_path,
                download_url=download_url,
                md5_hash=md5_hash,
            )
        else:
            raise ValueError(f'font type "{type(font)}" is not supported.')

        lnoptions: dict = {"line_numbers": show_linenum}
        if show_linenum:
            lnoptions["line_number_fg"] = ColorUtil.get_hexrgb(linenum_textcolor)
            lnoptions["line_number_bg"] = ColorUtil.get_hexrgb(linenum_bgcolor)

        return ImageFormatter(
            style=pygments_style,
            font_name=file_path,
            **lnoptions,
        )
