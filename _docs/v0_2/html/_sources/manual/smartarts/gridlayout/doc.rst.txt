=============
GridLayout
=============

Class `dsart.GridLayout` draws smart art grid layouted rectangles.

.. figure:: image1.png
    :width: 600
    :class: with-border
    :align: center

    image1.png

You can draw grid layout with these procedure.

1. Initialize instance with specifying number of columns and rows.
2. Add grid layout items with optional custom style
3. Draw pyramid with specified position, size and alignment.


API Specification
=====================

dsart.GridLayout()
-------------------

Initializes a GridLayout instance.

Args:

- num_column (int): The number of columns in the grid.
- num_row (int): The number of rows in the grid.
- default_r (int, optional): The default radius for the rectangles. Defaults to 0.
- default_style (Union[str, ShapeStyle, None], optional): The default style for the rectangles. Can be a string key, a ShapeStyle object, or None. Defaults to None.
- default_textstyle (Union[str, ShapeTextStyle, None], optional): The default text style for the rectangles. Can be a string key, a ShapeTextStyle object, or None. Defaults to None.
- default_textangle (Optional[float], optional): The default angle for the text inside the rectangles. If None, no angle is applied. Defaults to None.

add()
--------

Add an item to the grid layout.

Args:

- position (Tuple[int, int]): Cell start (column, row) point.
- width (int): How many column cells.
- height (int): How many row cells.
- r (Optional[int], optional): The radius of the item. Default is None, which uses the default radius.
- style (Union[str, ShapeStyle, None], optional): The style of the item. Can be a string key for a predefined style, a ShapeStyle object, or None to use the default style.
- text (str, optional): The text associated with the item. Default is an empty string.
- textstyle (Union[str, ShapeTextStyle, None], optional): The text style of the item. Can be a string key for a predefined text style, a ShapeTextStyle object, or None to use the default text style.
- textangle (Optional[float], optional): The angle of the text. Default is None, which is same to 0.
- text_xy_shift (Optional[Tuple[float, float]], optional): The XY shift of the text. Default is None, which is same to (0, 0).

draw()
--------

Draw the grid layout.

Args:

- xy (Tuple[float, float]): The x and y coordinates of the top-left corner of the grid.
- width (float): The total width of the grid.
- height (float): The total height of the grid.
- margin (float): The margin between grid items.
- outer_r (int, optional): The radius for the outer grid border. Default is 0.
- outer_style (Union[str, ShapeStyle, None], optional): The style for the outer grid border. Can be a string key for a predefined style, a ShapeStyle object, or None.

draw_flexible()
-----------------

Draw the grid layout with flexible column widths and row heights.

Args:

- xy (Tuple[float, float]): The x and y coordinates of the top-left corner of the grid.
- column_widths (List[float]): The widths of each column.
- column_margins (List[float]): The margins between columns.
- row_heights (List[float]): The heights of each row.
- row_margins (List[float]): The margins between rows.
- outer_r (int, optional): The radius for the outer grid border. Default is 0.
- outer_style (Union[str, ShapeStyle, None], optional): The style for the outer grid border. Can be a string key for a predefined style, a ShapeStyle object, or None.

