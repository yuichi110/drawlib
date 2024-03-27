"""module for handling cache"""

from typing import Dict
from drawlib._model import (
    LineStyle,
    ShapeStyle,
    TextStyle,
    TextBackgroundStyle,
)
from drawlib._pil import Pimage
from drawlib._util import error_handler


class Cache:
    """class for handling cache"""

    def __init__(self) -> None:
        self._line_styles: Dict[str, LineStyle] = {}
        self._shape_styles: Dict[str, ShapeStyle] = {}
        self._text_styles: Dict[str, TextStyle] = {}
        self._textbackground_styles: Dict[str, TextBackgroundStyle] = {}
        self._pimages: Dict[str, Pimage] = {}

    ##################
    ### line style ###
    ##################

    @error_handler
    def has_cache_linestyle(self, name: str) -> bool:
        """write docstring later"""

        return name in self._line_styles

    @error_handler
    def set_cache_linestyle(self, name: str, style: LineStyle) -> None:
        """write docstring later"""

        self._line_styles[name] = style

    @error_handler
    def get_cache_linestyle(self, name: str) -> LineStyle:
        """write docstring later"""

        if not self.has_cache_linestyle(name):
            raise ValueError(f'LineStyle "{name}" is not cached.')
        return self._line_styles[name]

    ###################
    ### shape style ###
    ###################

    @error_handler
    def has_cache_shapestyle(self, name: str) -> bool:
        """write docstring later"""

        return name in self._shape_styles

    @error_handler
    def set_cache_shapestyle(self, name: str, style: ShapeStyle) -> None:
        """write docstring later"""

        self._shape_styles[name] = style

    @error_handler
    def get_cache_shapestyle(self, name: str) -> ShapeStyle:
        """write docstring later"""

        if not self.has_cache_shapestyle(name):
            raise ValueError(f'ShapeStyle "{name}" is not cached.')
        return self._shape_styles[name]

    ##################
    ### text style ###
    ##################

    @error_handler
    def has_cache_textstyle(self, name: str) -> bool:
        """write docstring later"""

        return name in self._text_styles

    @error_handler
    def set_cache_textstyle(self, name: str, style: TextStyle) -> None:
        """write docstring later"""

        self._text_styles[name] = style

    @error_handler
    def get_cache_textstyle(self, name: str) -> TextStyle:
        """write docstring later"""

        if not self.has_cache_textstyle(name):
            raise ValueError(f'TextStyle "{name}" is not cached.')
        return self._text_styles[name]

    #############################
    ### text background style ###
    #############################

    @error_handler
    def has_cache_textbackgroundstyle(self, name: str) -> bool:
        """write docstring later"""

        return name in self._textbackground_styles

    @error_handler
    def set_cache_textbackgroundstyle(
        self,
        name: str,
        style: TextBackgroundStyle,
    ) -> None:
        """write docstring later"""

        self._textbackground_styles[name] = style

    @error_handler
    def get_cache_textbackgroundstyle(self, name: str) -> TextBackgroundStyle:
        """write docstring later"""

        if not self.has_cache_textbackgroundstyle(name):
            raise ValueError(f'TextBackgroundStyle "{name}" is not cached.')
        return self._textbackground_styles[name]

    #############
    ### image ###
    #############

    @error_handler
    def has_cache_image(self, name: str) -> bool:
        """write docstring later"""

        return name in self._pimages

    @error_handler
    def set_cache_image(self, name: str, image: Pimage) -> None:
        """write docstring later"""

        self._pimages[name] = image.copy()

    @error_handler
    def get_cache_image(self, name: str) -> Pimage:
        """write docstring later"""

        if not self.has_cache_image(name):
            raise ValueError(f'Pimage "{name}" is not cached.')
        return self._pimages[name].copy()


__c = Cache()

# line style
has_cache_linestyle = __c.has_cache_linestyle
set_cache_linestyle = __c.set_cache_linestyle
get_cache_linestyle = __c.get_cache_linestyle

# shape style
has_cache_shapestyle = __c.has_cache_shapestyle
set_cache_shapestyle = __c.set_cache_shapestyle
get_cache_shapestyle = __c.get_cache_shapestyle

# text style
has_cache_textstyle = __c.has_cache_textstyle
set_cache_textstyle = __c.set_cache_textstyle
get_cache_textstyle = __c.get_cache_textstyle

# text background style
has_cache_textbackgroundstyle = __c.has_cache_textbackgroundstyle
set_cache_textbackgroundstyle = __c.set_cache_textbackgroundstyle
get_cache_textbackgroundstyle = __c.get_cache_textbackgroundstyle

# pimage
has_cache_image = __c.has_cache_image
set_cache_image = __c.set_cache_image
get_cache_image = __c.get_cache_image
