from typing import Final, Union, Optional, List, Tuple, Dict, Any, Literal
import matplotlib.font_manager
import matplotlib.artist
import matplotlib.lines
import matplotlib.text
import matplotlib.pyplot as pyplot
from matplotlib.artist import Artist
from matplotlib.axes import Axes
import PIL.Image
import inspect
import os

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
from drawlib._core.patches import (
    get_circle,
    get_rectangle,
    get_rectangle_rounded,
)
from drawlib._core.text import (
    get_text,
    get_text_vertical,
)
from drawlib._core.util import (
    get_font_properties,
)


class __DrawingState:
    DEFAULT_WIDTH: Final[float] = 100
    DEFAULT_HEIGHT: Final[float] = 100
    DEFAULT_GRID: Final[bool] = False
    DEFAULT_LOGLEVEL: Final[str] = "info"
    SYSTEM_FONTS = ["serif", "sanserif"]

    class Title:
        def __init__(
            self,
            text: str,
            x: Optional[float] = None,
            y: Optional[float] = None,
            fontproperties: Optional[matplotlib.font_manager.FontProperties] = None,
        ):
            self.text = text
            self.x = x
            self.y = y
            self.fontproperties = fontproperties

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
        self.__init__()

    @error_handler
    def config(
        self,
        width: int | None = None,
        height: int | None = None,
        grid: bool | None = None,
        grid_style: Optional[LineStyle] = None,
    ) -> None:
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if grid is not None:
            self.grid = grid

    @error_handler
    def get_matplotlib_ax(self) -> Axes:
        return self._ax

    @error_handler
    def add_matplotlib_artist(self, artist: Artist):
        self._artists.append(artist)

    @error_handler
    def plot(self):
        self._render()
        pyplot.show()

    @error_handler
    def save(self, file: Optional[str] = None):
        if file is None:
            # get caller module info
            caller_frame = inspect.stack()[1]
            caller_module = inspect.getmodule(caller_frame[0])
            caller_module_file = caller_module.__file__
            caller_module_name = caller_module.__name__

            # create save file path
            parent_dir = os.path.dirname(os.path.abspath(caller_module_file))
            file_name = caller_module_name.split(".")[-1]
            file = f"{os.path.join(parent_dir, file_name)}.png"

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
    ): ...

    @error_handler
    def arrow(self): ...

    @error_handler
    def arrow_fancy(self): ...

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
    def ellipse(self): ...

    @error_handler
    def polygon(self): ...

    @error_handler
    def polygon_circle(self): ...

    @error_handler
    def polygon_regular(self): ...

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
        rtype: Optional[Literal["round", "round4", "sawtooth", "roundtooth"]] = None,
        pad: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        angle: Optional[float] = None,
        text: Optional[str] = None,
        textstyle: Optional[TextStyle] = None,
    ):
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
    def wedge(self): ...

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
    def text_vertical(self, x: float, y: float, s: str): ...

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
        line_ = get_line(x1, y1, x2, y2, style)
        self._artists.append(line_)

    @error_handler
    def lines(
        self,
        xys: List[Tuple[float, float]],
        style: Optional[LineStyle] = None,
    ):
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
        raise Exception("hello")
        line_ = get_line_bezier(x, y, bezier_points, smooth_points, style)
        self._artists.append(line_)


__d = __DrawingState()
# basics
clear = __d.clear
config = __d.config
plot = __d.plot
save = __d.save
title = __d.title
get_matplotlib_ax = __d.get_matplotlib_ax
add_matplotlib_artist = __d.add_matplotlib_artist

# patched
circle = __d.circle
shape_circle = circle
rectangle = __d.rectangle
shape_rectangle = rectangle
rectangle_rounded = __d.rectangle_rounded
shape_rectangle_rounded = rectangle_rounded

# text
text = __d.text

# image
image = __d.image

# line
line = __d.line
lines = __d.lines
line_bezier = __d.line_bezier
