=================================
Drawlib from a High Perspective
=================================

Drawing illustrations can be a complex task, but Drawlib aims to simplify this process by providing a range of APIs for drawing icons, images, lines, shapes, and text, complete with various styles.
You don't need to memorize every detail to start drawing; understanding the library's design allows you to write efficient code. 
IDEs can assist by providing quick access to classes, functions, and their options.

If you encounter difficulties, our API documentation offers comprehensive guidance on usage.

Abstract API Structure
======================

Drawlib is structured around the following APIs:

- Fundamental classes and functions: These include essential canvas manipulation methods such as ``save()`` and ``config()``.
- Drawing functions: Examples include ``circle()`` and ``line()``.
- Style classes: Categories like ``ShapeStyle`` and ``LineStyle`` define the visual appearance of elements.
- Theme and style accessor module (``dtheme``): This module facilitates managing themes and accessing styles across drawings.
- Advanced classes and functions: These components utilize the aforementioned APIs internally to provide extended functionality.

.. figure:: image1.png
    :width: 600
    :class: with-border
    :align: center

    image1.png

The image above illustrates Drawlib's core components, categorized into five sections representing its various APIs. 
Despite its complexity, Drawlib maintains consistency in function arguments and style classes.

Once you grasp the fundamental concepts of the library, predicting the outcomes of functions and arguments becomes intuitive.
