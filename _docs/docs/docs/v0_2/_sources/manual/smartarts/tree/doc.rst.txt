=============
Tree
=============

Class ``dsart.Tree`` draws smart art tree which is similar to ``tree`` command output.

.. figure:: image1.png
    :width: 600
    :class: with-border
    :align: center

    image1.png

Each Tree instances are nodes of tree structure.
Node can contain children nodes and able to override the style.

You can draw tree with these procedure.

1. Create root tree node
2. Add children nodes
3. Draw tree with providing coordinate

API Specification
======================

``dsart.Tree()``
--------------------------

Initializes a TreeNode instance with specific text, styles, and optional children.
Styles are mandatory for root node. Optional for child nodes.

Args:

- text (str): The text content for the tree node.
- textstyle (Union[str, TextStyle, None], optional): The text style for the node. It can be a string that maps to a `TextStyle` or a `TextStyle` instance. Defaults to None.
- linestyle (Union[str, LineStyle, None], optional): The line style for the node. It can be a string that maps to a `LineStyle` or a `LineStyle` instance. Defaults to None.
- line_horizontal_margin (Optional[float], optional): The margin for horizontal lines. Defaults to None.
- line_horizontal_length (Optional[float], optional): The length of horizontal lines. Defaults to None.
- line_vertical_margin (Optional[float], optional): The margin for vertical lines. Defaults to None.
- children (Optional[List[TreeNode]], optional): A list of child nodes connected to this node. Defaults to None.
- default_textstyle (Union[str, TextStyle, None], optional): The default text style for child nodes. Defaults to None.
- default_linestyle (Union[str, LineStyle, None], optional): The default line style for child nodes. Defaults to None.
- default_line_horizontal_margin (Optional[float], optional): The default horizontal margin for lines of child nodes. Defaults to None.
- default_line_horizontal_length (Optional[float], optional): The default horizontal length for lines of child nodes. Defaults to None.
- default_line_vertical_margin (Optional[float], optional): The default vertical margin for lines of child nodes. Defaults to None.

``register_drawing_item()``
-----------------------------

Class method.
Register a drawing item for the tree node.
This class returns current tree node instance.

Args:

- name (str): Name of drawing item.
- location (Literal["before", "after"]): The location of the drawing item relative to the text.
- padding_width (float): The padding width for the drawing item.
- function (Callable): The function to render the drawing item.
- style (Union[IconStyle, ImageStyle, ShapeStyle, TextStyle]): The style for the drawing item.
- args (dict): The arguments for the function.


``set_drawing_item()``
------------------------

Set a drawing item for the tree node.

Args:
            
- name (str): Name of drawing item.

``draw()``
-----------

Draw the tree node and its children.
ValueError is raised if any of the default styles or margins are None.

Args:

- xy (Tuple[float, float]): The coordinates to start drawing.

