=================
Advanced Topics
=================

In this section, we will cover advanced theme topics that are not addressed in the foundational chapter's theme section.

Accessing Theme Styles Manually
=================================

Theme styles are typically used as follows: ``text(xy=(10,10), text="Hello Drawlib!", style="blue")``. 
However, you can also access the style manually through the dtheme module functions.

Each style is stored in a cache object within ``dtheme.<type>styles``, where the name corresponds to Drawlib's style class name. 
Here are the major objects:

- ``IconStyle``: ``dtheme.iconstyles``
- ``ImageStyle``: ``dtheme.imagestyles``
- ``LineStyle``: ``dtheme.linestyles``
- ``LineArrowStyle``: ``dtheme.linearrowstyles``
- ``ShapeStyle``: ``dtheme.shapestyles``
- ``ShapeTextStyle``: ``dtheme.shapetextstyles``
- ``TextStyle``: ``dtheme.textstyles``

Each style cache object possesses these methods:

- ``has(name)``: Checks whether the named style exists.
- ``list()``: Retrieves the names of styles.
- ``get(name)``: Retrieves the style object.
- ``set(style, name)``: Sets the style object.
- ``delete(name)``: Deletes the style object.
- ``merge(style, targets)``: Merges the style with the targets (explained later).

These methods are called internally in the drawing functions. 
Manual access to theme styles is useful in the following situations:

- Getting and modifying theme styles.
- Setting updated theme styles.
- Customizing by getting, modifying, and then setting the style.

Here is an example of these three operations:

.. literalinclude:: image_access1.py
   :language: python
   :linenos:
   :caption: image_access1.py

Executing the code generates the following output:

.. figure:: image_access1.png
   :width: 600
   :class: with-border
   :align: center

   Specifying theme style name

You can manually modify any styles using these methods. 
However, please prioritize higher-level methods such as ``merge()``, etc.


Customize Styles for Each Shape
----------------------------------

Drawlib allows you to customize styles for individual shape objects such as ``circle()`` and ``rectangle()``. 
``dtheme`` maintains a style cache object for each shape type. 
For example, there are these objects:

- dtheme.circlestyles
- dtheme.rectanglestyles

These objects function similarly to ``dtheme.shapestyles``. 
However, specific shape style objects have higher priority than general shape style objects. 
For instance, if you call ``circle(xy=(50, 50), radius=20, style="red")``, the circle function will search for the theme style in this order:

1. Check if ``dtheme.circlestyles`` has the key "red". If yes, apply it.
2. Check if ``dtheme.shapestyles`` has the key "red". If yes, apply it.
3. Raise a not found exception.

Regarding ``ShapeTextStyle``, it will behave similarly. 
``dtheme`` contains ``dtheme.circletextstyles`` and ``dtheme.shapetextstyles``. 
The former has higher priority in the ``circle()`` function.


Override Theme's Style with ``merge()``
=========================================

In the previous example, we updated the theme's style by following the process of getting, changing, and setting. 
We can also achieve updates through the ``merge()`` function.

The ``merge()`` function is implemented in ``dtheme.<type>styles``, as previously explained. 
For example, ``dtheme.textstyles.merge()``.

This function takes two arguments:

- ``style``: The style object to merge.
- ``targets`` (optional): A list of style names.

The provided style is merged with the targets. 
If no targets are provided, the style is merged with all styles.

Here is an example of merging a text style:

.. literalinclude:: image_merge1.py
   :language: python
   :linenos:
   :caption: image_merge1.py

In this example, we change the text fonts. 
Executing the code generates the following output:

.. figure:: image_merge1.png
   :width: 600
   :class: with-border
   :align: center

The image's text is updated to the new fonts.

``dtheme.allstyles.merge()``
------------------------------

In the previous example, we only changed the text style. 
If you want to customize multiple types of styles simultaneously, you can use ``dtheme.allstyles.merge()``. 
This function takes two arguments:

- ``theme_style``: A ``dtheme.ThemeStyle`` object that holds multiple style types.
- ``targets`` (optional): A list of style names.

If the style object is held in the ``ThemeStyle`` object, the theme style that matches the targets is merged.

Here is an example of merging both line and text styles at the same time:

.. literalinclude:: image_merge2.py
   :language: python
   :linenos:
   :caption: image_merge2.py

In this example, we change the line width and text fonts. 
Executing the code generates the following output:

.. figure:: image_merge2.png
   :width: 600
   :class: with-border
   :align: center

If you need to change multiple styles with the same style name, this function is very useful.


Rename Style Name
=====================

Drawlib's official theme provides style names that start with colors, such as ``red``, ``red_solid``, and ``red_bold``. 
If you hardcode these names into your illustration code, changing the color later would require extensive modifications to your code.

Using color names is fine if the color itself has meaning. 
However, if you want to maintain color consistency like this:

- Primary color: blue
- Secondary color: green
- Tertiary color: red

You should rename the theme style names and use the new names in your illustration codes. 
For example:

- Rename blue to "1"
- Rename green to "2"
- Rename red to "3"

By doing this, changing the primary color becomes easy because you don't need to change the illustration code, just the style code. 
For instance:

- Rename red to "1"
- Rename green to "2"
- Rename blue to "3"

To change the style name, you can use the ``dtheme.allstyles`` object, which provides methods for modifying style names. 
Here is the list of methods:

- ``rename(from_name, to_name)``: Renames the style name.
- ``copy(from_name, to_name)``: Copies the style name and its object.
- ``delete(name)``: Deletes the style name.
- ``merge()``: As explained previously.

In our situation, we should use ``dtheme.allstyles.rename()``. 
Let's look at an example.

Here is the original code:

.. literalinclude:: image_rename1.py
   :language: python
   :linenos:
   :caption: image_rename1.py

First, we rename the theme styles in the style code. 
Then, we use the new names in the illustration codes. 

This generates the following output:

.. figure:: image_rename1.png
    :width: 600
    :class: with-border
    :align: center

Suppose you want to change the theme to ``essentials`` and update the colors. 

Here is the new code:

.. literalinclude:: image_rename2.py
   :language: python
   :linenos:
   :caption: image_rename2.py

We rename the theme style names again at the beginning of the code. 
Notice that we rename them to the same style names "1", "2", "3".

The illustration code remains exactly the same as in the previous example since it references the same style names "1", "2", "3". 

This generates the following output:

.. figure:: image_rename2.png
    :width: 600
    :class: with-border
    :align: center

Without changing the illustration code, which is located at the bottom, we can achieve a different style output.

In this example, we included both the style code and illustration code in a single file. 
However, style code and illustration code are usually separated. 
This means you can achieve new style images without changing the illustration codes.


Accessing Theme Colors
=======================

When you add a style object to the current theme, you may want to reference the theme colors. 
Drawlib provides the ``dtheme.colors`` object for this purpose.

The ``dtheme.colors`` object functions similarly to the previous style cache objects and includes the following methods:

- ``has(name)``: Checks whether the named color exists.
- ``list()``: Retrieves the names of colors.
- ``get(name)``: Retrieves the color.
- ``set(color, name)``: Sets the color.
- ``delete(name)``: Deletes the color.

Here is an example of accessing style colors:

.. literalinclude:: image_colors1.py
   :language: python
   :linenos:
   :caption: image_colors1.py

As you can see, you can get a list of color names and retrieve the RGBA values from a color name.