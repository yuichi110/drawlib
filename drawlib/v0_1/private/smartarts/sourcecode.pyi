"""
This type stub file was generated by pyright.
"""

from typing import Final, Literal, Optional, Tuple, Union
from drawlib.v0_1.private.core.dimage import Dimage
from drawlib.v0_1.private.core.fonts import FontFile, FontSourceCode
from drawlib.v0_1.private.core.model import ImageStyle
from drawlib.v0_1.private.util import error_handler

"""SourceCode implementation module."""
PYGMENTS_LINENUM_TEXT_COLOR: Final[Tuple[int, int, int]] = ...
PYGMENTS_LINENUM_BACKGROUND_COLOR: Final[Tuple[int, int, int]] = ...
class SourceCode:
    """Class for rendering source code as an image using Pygments.

    This class allows you to configure the style and font of the rendered source code image.
    You can render the source code image using the `draw()` method or obtain the image
    directly with the `get_image()` method.
    """
    @error_handler
    def __init__(self, language: Optional[Literal["bash", "c", "c#", "c++", "coffeescript", "css", "dart", "docker", "go", "groovy", "haskell", "html", "ini", "java", "javascript", "json", "julia", "kotlin", "less", "markdown", "none", "objective-c", "perl", "php", "plain", "powershell", "promql", "protobuf", "python", "restructuredtext", "ruby", "rust", "sql", "swift", "tex", "text", "toml", "typescript", "verilog", "xml", "yaml",]] = ..., style: Literal["bw", "sas", "staroffice", "xcode", "default", "monokai", "lightbulb", "github-dark", "rrt", "algol", "algol_nu", "friendly_grayscale",] = ..., font: Union[FontSourceCode, FontFile, None,] = ..., show_linenum: bool = ..., linenum_textcolor: Union[Tuple[int, int, int], Tuple[int, int, int, float],] = ..., linenum_bgcolor: Union[Tuple[int, int, int], Tuple[int, int, int, float],] = ...) -> None:
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
        ...
    
    @error_handler
    def get_image(self, code: str) -> Dimage:
        """Generate an image of the source code.

        Args:
            code (str): The source code to render.

        Returns:
            Dimage: The generated image of the source code.

        """
        ...
    
    @error_handler
    def draw(self, xy: Tuple[float, float], width: float, code: str, style: Optional[ImageStyle] = ...) -> None:
        """Draw the source code image on a canvas.

        Args:
            xy (Tuple[float, float]): The (x, y) coordinates for the top-left corner of the image.
            width (float): The width of the image.
            code (str): The source code to render.
            style (Optional[ImageStyle]): The style to apply to the image.

        """
        ...
    
    @staticmethod
    @error_handler
    def get_text(file: str, strip: bool = ...) -> str:
        """Retrieve the text from a file.

        Args:
            file (str): The path to the file.
            strip (bool): Whether to strip leading and trailing whitespace.

        Returns:
            str: The contents of the file.

        """
        ...
    


