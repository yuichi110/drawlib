# BoxList


`drawlib.smartarts.BoxList` renders sequentially chained lists of boxed cards or sequence registers. It is commonly used for array visualizations, queue states, execution pipelines, and horizontal/vertical stage progressions.

---

## 1. Quick Start

Create a `BoxList`, append or extend items, and render them with `draw()`:

```drawlib show-code 650px center caption:"BoxList Layout & Custom Styling"
from drawlib.canvas import config
from drawlib.smartarts import BoxList

config(width=100, height=45)

# 1. Horizontal list (Left to Right)
b1 = BoxList(default_text_style="white")
b1.extend(["1", "2", "3", "4"])
b1.draw(xy=(10, 30), box_width=8, box_height=6)

# 2. Custom box styling & highlighted elements
b2 = BoxList(default_box_style="solid", default_text_style="")
b2.extend(["1", "2"])
b2.append("3", box_style="red_solid_bold", text_style="red_bold")
b2.extend(["4", "", ""])
b2.draw(xy=(10, 10), box_width=8, box_height=6)

# 3. Vertical list (Bottom to Top)
b3 = BoxList(default_text_style="white")
b3.extend(["1", "2", "3", "4"])
b3.draw(xy=(75, 10), box_width=8, box_height=6, align="bottom")
```

---

## 2. Alignment and Orientation

`BoxList` supports 4 alignment directions from the anchor coordinate `xy`:
- **`left`** (default): Extends horizontally to the right.
- **`right`**: Extends horizontally to the left.
- **`bottom`**: Stacks vertically upwards.
- **`top`**: Stacks vertically downwards.

---



# API Specification



## ``BoxList()``


Initialize BoxList.

Args.

- default_box_style (Union[str, Style, None]): The style for the boxes.
- default_text_style (Union[str, Style, None]): The style for the text inside the boxes.


## ``append()``


Appends a new box with text to the BoxList.

Args:

- text (str): The text to be displayed inside the box.
- box_style (Union[str, Style, None], optional): The style for the box. Can be a style name, a Style object, or None. If None, the default box style is used.
- text_style (Union[str, Style, None], optional): The style for the text inside the box. Can be a style name, a Style object, or None. If None, the default text style is used.


## ``insert()``


Inserts a new box with text at a specified position in the BoxList.

Args:

- index (int): The position at which to insert the new box.
- text (str): The text to be displayed inside the box.
- box_style (Union[str, Style, None], optional): The style for the box. Can be a style name, a Style object, or None. If None, the default box style is used.
- text_style (Union[str, Style, None], optional): The style for the text inside the box. Can be a style name, a Style object, or None. If None, the default text style is used.


## ``extend()``


Extends the BoxList by appending multiple boxes with text.

Args:

- texts (List[str]): A list of texts to be displayed inside the boxes.
- box_style (Union[str, Style, None], optional): The style for the boxes. Can be a style name, a Style object, or None. If None, the default box style is used.
- text_style (Union[str, Style, None], optional): The style for the text inside the boxes. Can be a style name, a Style object, or None. If None, the default text style is used.


## ``draw()``


Draws a list of boxes at the specified location.

Args:

- xy (Tuple[float, float]): The starting point (x, y) to draw the list of boxes.
- box_width (float): The width of each box.
- box_height (float): The height of each box.
- align (Literal["left", "right", "bottom", "top"]): The alignment of the boxes relative to the starting point.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
