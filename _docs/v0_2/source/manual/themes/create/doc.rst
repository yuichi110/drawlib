========================================
Create Your Custom Theme from Scratch
========================================

We provide official themes that you can customize to fit your needs. 
Consider customizing our themes first if you only need to make slight style changes.

However, some users may prefer to create their own custom theme entirely from scratch. 
You can achieve this by following these procedures:

- Create Your Theme's Default Styles: Define the fundamental styles that will form the basis of your theme.
- Optional: Create Named Theme Styles: Optionally, define named theme styles such as "blue", "blue_solid" to customize specific elements further.
- Optional: Define Background Color and Source Code Font: Set preferences for background color and source code font if desired.
- Apply Your Custom Theme: Pass your defined styles and preferences to ``dtheme.apply_custom_theme()`` to apply your custom theme.

The ``dtheme.apply_custom_theme()`` function accepts the following arguments:

- ``default_style``: Default styles for your theme.
- ``named_styles`` (optional): Named styles within your theme, e.g., "blue".
- ``theme_colors`` (optional): List of colors used in your theme.
- ``backgroundcolor`` (optional): Background color of your theme.
- ``sourcecodefont`` (optional): Default font for displaying source code.

Let's go through these steps in detail.

Create ``ThemeStyles`` Object
===============================

The ``default_style`` and ``named_styles`` arguments require a ``dtheme.ThemeStyles`` object. 
This class serves as a container for Drawlib's styles such as ``LineStyle``, ``ShapeStyle``, etc.

When defining your data, populate the ``default_style`` object with the following mandatory items:

- iconstyle
- imagestyle
- linestyle
- linearrowstyle
- shapestyle
- shapetextstyle
- textstyle

Other items are optional for the ``default_style``, and all items are optional for ``named_styles``.



Apply Theme Styles
====================

Once you have defined your ``ThemeStyles`` objects, pass them to ``dtheme.apply_custom_theme()``. 
This function clears old theme styles internally before applying your new custom theme.

Here's an example script demonstrating the creation of a gold and silver themed custom theme:

.. literalinclude:: image1.py
   :language: python
   :linenos:
   :caption: image1.py

In this example, we define ``ThemeStyles`` for gold and silver themes and apply them using ``dtheme.apply_custom_theme()``.

Executing this script will produce the following output:

.. figure:: image1.png
    :width: 600
    :class: with-border
    :align: center

    Drawing items with custom theme

You can observe that the default style of the theme has been set to gold, and the named styles "gold" and "silver" are also applied.

Recommendation
=================

While you have the flexibility to create your own theme, it is recommended to adhere to Drawlib's official style guidelines when sharing themes to ensure consistency and compatibility.