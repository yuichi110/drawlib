"""write docstring later"""

# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods

# !!! Temporary Lint Escape !!!
# pylint: disable=unnecessary-ellipsis
# pylint: disable=unused-argument

import os
import dataclasses
from typing import Final, Union, Optional, List, Tuple, Literal
import matplotlib.font_manager
import matplotlib.artist
import matplotlib.lines
import matplotlib.text
from matplotlib import pyplot
from matplotlib.artist import Artist
from matplotlib.axes import Axes
import PIL.Image


from drawlib._util import error_handler
from drawlib._model import (
    LineStyle,
    ShapeStyle,
    TextStyle,
    TextBackgroundStyle,
)
from drawlib._core.image import (
    get_image,
)
from drawlib._core.line import (
    get_line,
    get_lines,
    get_line_bezier,
)
from drawlib._core.shape import (
    get_circle,
    get_rectangle,
    get_rectangle_rounded,
)
from drawlib._core.text import (
    get_text,
    # get_text_vertical,
)
from drawlib._core.util import (
    get_font_properties,
)
from drawlib._util import (
    get_user_script_path,
    get_script_relative_path,
)


class Canvas:
    """write docstring later"""

    DEFAULT_WIDTH: Final[float] = 100
    DEFAULT_HEIGHT: Final[float] = 100
    DEFAULT_GRID: Final[bool] = False
    DEFAULT_LOGLEVEL: Final[str] = "info"
    SYSTEM_FONTS = ["serif", "sanserif"]

    @dataclasses
    class Title:  # pylint: disable=too-few-public-methods
        """write docstring later"""

        text: str
        x: Optional[float] = None
        y: Optional[float] = None
        fontproperties: Optional[matplotlib.font_manager.FontProperties] = None

    @error_handler
    def __init__(self):
        self.width = self.DEFAULT_WIDTH
        self.height = self.DEFAULT_HEIGHT
        self.grid = self.DEFAULT_GRID
        self.loglevel = self.DEFAULT_LOGLEVEL

        self._fig = pyplot.figure()
        self._ax = self._fig.add_subplot(1, 1, 1)
        self._title: Optional[self.Title] = None
        self._logger = None
        self._artists: List[matplotlib.artist.Artist] = []

    ##############
    ### basics ###
    ##############

    @error_handler
    def clear(self):
        """write docstring later"""

        # initialize again without changing object itself
        self.__init__()  # pylint: disable=unnecessary-dunder-call

    @error_handler
    def config(
        self,
        width: int | None = None,
        height: int | None = None,
        grid: bool | None = None,
        grid_style: Optional[LineStyle] = None,
    ) -> None:
        """write docstring later"""

        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if grid is not None:
            self.grid = grid

    @error_handler
    def get_matplotlib_ax(self) -> Axes:
        """write docstring later"""

        return self._ax

    @error_handler
    def add_matplotlib_artist(self, artist: Artist):
        """write docstring later"""

        self._artists.append(artist)

    @error_handler
    def plot(self):
        """write docstring later"""

        self._render()
        pyplot.show()

    @error_handler
    def save(self, file: Optional[str] = None):
        """write docstring later"""

        if file is None:
            script_path = get_user_script_path()
            parent_dir = os.path.dirname(script_path)
            name = os.path.basename(script_path)
            name_without_ext = os.path.splitext(name)[0]
            file = f"{os.path.join(parent_dir, name_without_ext)}.png"

        else:
            file = get_script_relative_path(file)

        # rendering
        self._render()

        # prepare directory if not exist
        directory = os.path.dirname(file)
        os.makedirs(directory, exist_ok=True)

        # save
        pyplot.savefig(file, bbox_inches="tight")

    @error_handler
    def _render(self):
        fig = self._fig
        ax = self._ax

        # configure
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect("equal")
        if self.grid:
            ax.axis("on")
            ax.grid(visible=True, which="both", axis="both")
        else:
            ax.axis("off")
            ax.grid(visible=False)

        # draw artist (patches, line, text)
        for artist in self._artists:
            ax.add_artist(artist)

        # draw title
        if self._title is not None:
            options = {
                key: value
                for key, value in vars(self._title).items()
                if value is not None
            }
            ax.set_title(self._title.text, **options)

        # magic for making good margin
        fig.tight_layout()

    @error_handler
    def title(
        self,
        text: str,
        x: Optional[float] = None,
        y: Optional[float] = None,
        style: Optional[TextStyle] = None,
    ):
        """write docstring later"""

        fp = get_font_properties(style)
        self._title = self.Title(text, x, y, fp)

    ####################
    ### _core.patchs ###
    ####################

    @error_handler
    def arc(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        angle: float = 0,
    ):
        """write docstring later"""
        ...

    @error_handler
    def arrow(self):
        """write docstring later"""
        ...

    @error_handler
    def arrow_fancy(self):
        """write docstring later"""
        ...

    @error_handler
    def circle(
        self,
        x: float,
        y: float,
        radius: float,
        style: Optional[ShapeStyle] = None,
        angle: Optional[float] = None,
        text: Optional[str] = None,
        textstyle: Optional[TextStyle] = None,
    ):
        """write docstring later"""

        circle_, text_ = get_circle(
            x=x,
            y=y,
            radius=radius,
            style=style,
            angle=angle,
            text=text,
            textstyle=textstyle,
        )
        self._artists.append(circle_)
        if text_ is not None:
            self._artists.append(text_)

    @error_handler
    def ellipse(self):
        """write docstring later"""
        ...

    @error_handler
    def polygon(self):
        """write docstring later"""
        ...

    @error_handler
    def polygon_circle(self):
        """write docstring later"""
        ...

    @error_handler
    def polygon_regular(self):
        """write docstring later"""
        ...

    @error_handler
    def rectangle(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        style: Optional[ShapeStyle] = None,
        angle: Optional[float] = None,
        text: Optional[str] = None,
        textstyle: Optional[TextStyle] = None,
    ):
        """write docstring later"""

        rectangle_, text_ = get_rectangle(
            x=x,
            y=y,
            width=width,
            height=height,
            style=style,
            angle=angle,
            text=text,
            textstyle=textstyle,
        )
        self._artists.append(rectangle_)
        if text_ is not None:
            self._artists.append(text_)

    @error_handler
    def rectangle_rounded(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        rtype: Optional[
            Literal["round", "round4", "sawtooth", "roundtooth"]
        ] = None,
        pad: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        angle: Optional[float] = None,
        text: Optional[str] = None,
        textstyle: Optional[TextStyle] = None,
    ):
        """write docstring later"""

        if angle is None:
            ax_and_angle = None
        else:
            ax_and_angle = (self._ax, angle)

        rectangle_, text_ = get_rectangle_rounded(
            x=x,
            y=y,
            width=width,
            height=height,
            rtype=rtype,
            pad=pad,
            style=style,
            ax_and_angle=ax_and_angle,
            text=text,
            textstyle=textstyle,
        )
        self._artists.append(rectangle_)
        if text_ is not None:
            self._artists.append(text_)

    @error_handler
    def wedge(self):
        """write docstring later"""
        ...

    ##################
    ### _core.text ###
    ##################

    @error_handler
    def text(
        self,
        x: float,
        y: float,
        text_: str,
        style: Optional[TextStyle] = None,
        background: Optional[TextBackgroundStyle] = None,
        angle: Optional[float] = None,
    ):
        """write docstring later"""

        self._artists.append(
            get_text(
                x=x,
                y=y,
                text=text_,
                style=style,
                background=background,
                angle=angle,
            )
        )

    @error_handler
    def text_vertical(self, x: float, y: float, s: str):
        """write docstring later"""
        ...

    ###################
    ### _core.image ###
    ###################

    @error_handler
    def image(
        self,
        x: float,
        y: float,
        file: Optional[str] = None,
        pilimg: Optional[PIL.Image.Image] = None,
        zoom=0.1,
    ):
        """write docstring later"""

        image_ = get_image(
            x=x,
            y=y,
            file=file,
            pilimg=pilimg,
            zoom=zoom,
        )
        self._artists.append(image_)

    ##################
    ### _core.line ###
    ##################

    @error_handler
    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        style: Optional[LineStyle] = None,
    ):
        """write docstring later"""

        line_ = get_line(x1, y1, x2, y2, style)
        self._artists.append(line_)

    @error_handler
    def lines(
        self,
        xys: List[Tuple[float, float]],
        style: Optional[LineStyle] = None,
    ):
        """write docstring later"""

        line_ = get_lines(xys, style)
        self._artists.append(line_)

    @error_handler
    def line_bezier(
        self,
        x: float,
        y: float,
        bezier_points: List[
            Union[
                Tuple[float, float],
                Tuple[float, float, float, float],
            ]
        ],
        smooth_points: int = 100,
        style: Optional[LineStyle] = None,
    ):
        """write docstring later"""

        line_ = get_line_bezier(x, y, bezier_points, smooth_points, style)
        self._artists.append(line_)


__c = Canvas()

# basics
clear = __c.clear
config = __c.config
plot = __c.plot
save = __c.save
title = __c.title
get_matplotlib_ax = __c.get_matplotlib_ax
add_matplotlib_artist = __c.add_matplotlib_artist

# shape
circle = __c.circle
rectangle = __c.rectangle
rectangle_rounded = __c.rectangle_rounded

# text
text = __c.text

# image
image = __c.image

# line
line = __c.line
lines = __c.lines
line_bezier = __c.line_bezier
